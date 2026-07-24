from django.db import transaction
from inventory.models import Stock, StockMovement
from .models import Order, OrderItem, OrderStatusHistory


class InsufficientStockError(Exception):
    pass


@transaction.atomic
def create_order_from_cart(cart, branch, source='online', placed_by=None,
                            shipping_address='', shipping_city='', shipping_phone=''):
    """
    Converts a Cart into an Order:
      1. Validates stock availability at the given branch
      2. Creates the Order + OrderItems (price-snapshotted)
      3. Decrements Stock and records a StockMovement for each item
      4. Marks the cart as checked out
    Wrapped in a DB transaction — if anything fails, nothing is committed
    (you never want a half-decremented stock or an order with no items).
    """
    cart_items = list(cart.items.select_related('variant').all())
    if not cart_items:
        raise ValueError("Cannot create an order from an empty cart.")

    # 1. Validate stock BEFORE making any changes
    stock_map = {}
    for item in cart_items:
        stock = Stock.objects.select_for_update().filter(
            variant=item.variant, branch=branch
        ).first()
        if not stock or stock.quantity < item.quantity:
            raise InsufficientStockError(
                f"Not enough stock for {item.variant} at {branch.name} "
                f"(have {stock.quantity if stock else 0}, need {item.quantity})"
            )
        stock_map[item.id] = stock

    # 2. Create the order
    order = Order.objects.create(
        store=cart.store,
        customer=cart.customer,
        branch=branch,
        source=source,
        placed_by=placed_by,
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_phone=shipping_phone,
        discount_amount=cart.discount_amount,
        coupon_code=cart.coupon.code if cart.coupon else '',
    )

    # 3. Create order items + decrement stock
    for item in cart_items:
        OrderItem.objects.create(
            store=cart.store,
            order=order,
            variant=item.variant,
            product_name=item.variant.product.name,
            unit_price=item.variant.current_price,
            quantity=item.quantity,
        )

        stock = stock_map[item.id]
        stock.quantity -= item.quantity
        stock.save(update_fields=['quantity'])

        StockMovement.objects.create(
            store=cart.store,
            variant=item.variant,
            branch=branch,
            reason='sale',
            quantity_change=-item.quantity,
            reference_id=order.order_number,
            performed_by=placed_by,
        )

    order.recalculate_totals()

    OrderStatusHistory.objects.create(store=cart.store, order=order, status='pending')

    if cart.coupon:
        cart.coupon.times_used += 1
        cart.coupon.save(update_fields=['times_used'])

    cart.is_abandoned = False
    cart.checked_out_at = order.created_at
    cart.save(update_fields=['is_abandoned', 'checked_out_at'])

    return order


@transaction.atomic
def update_order_status(order, new_status, changed_by=None, note=''):
    """
    Central place to change order status. Handles the one important side
    effect: if an order is cancelled/returned, stock must be restored.
    """
    if new_status in ('cancelled', 'returned') and order.status not in ('cancelled', 'returned'):
        for item in order.items.select_related('variant').all():
            stock, _ = Stock.objects.select_for_update().get_or_create(
                store=order.store, variant=item.variant, branch=order.branch,
                defaults={'quantity': 0}
            )
            stock.quantity += item.quantity
            stock.save(update_fields=['quantity'])

            StockMovement.objects.create(
                store=order.store, variant=item.variant, branch=order.branch,
                reason='return' if new_status == 'returned' else 'adjustment',
                quantity_change=item.quantity,
                reference_id=order.order_number,
                performed_by=changed_by,
                note=note or f"Order {new_status}",
            )

    order.status = new_status
    order.save(update_fields=['status'])

    OrderStatusHistory.objects.create(
        store=order.store, order=order, status=new_status,
        changed_by=changed_by, note=note
    )

    return order