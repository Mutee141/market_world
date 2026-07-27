import re

views_file = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\views.py'
with open(views_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace add_product variant logic
search_add = r'''            attributes = {}
            attr_model = request.POST.get('attr_model', '').strip()
            attr_variant = request.POST.get('attr_variant', '').strip()
            if attr_model:
                attributes['Model'] = attr_model
            if attr_variant:
                attributes['Variant'] = attr_variant
            
            with transaction.atomic():
                category = get_object_or_404(Category, store=request.store, id=category_id)
                brand = Brand.objects.filter(store=request.store, id=brand_id).first() if brand_id else None
                
                product = Product.objects.create(
                    store=request.store,
                    category=category,
                    brand=brand,
                    name=name,
                    description=description,
                    tags=tags,
                    status='active'
                )
                
                variant = ProductVariant.objects.create(
                    store=request.store,
                    product=product,
                    sku=sku,
                    cost_price=cost_price,
                    selling_price=selling_price,
                    discount_price=discount_price,
                    attributes=attributes,
                    is_active=True
                )
                
                if images:
                    for idx, img in enumerate(images):
                        ProductImage.objects.create(
                            store=request.store,
                            product=product,
                            image=img,
                            is_primary=(idx == 0),
                            order=idx + 1
                        )
                
                # Auto-initialize initial stock of 10 in default branch
                branch = Branch.objects.filter(store=request.store, is_default=True).first() or Branch.objects.filter(store=request.store).first()
                if branch:
                    Stock.objects.create(
                        store=request.store,
                        variant=variant,
                        branch=branch,
                        quantity=10,
                        low_stock_threshold=5
                    )
                    StockMovement.objects.create(
                        store=request.store,
                        variant=variant,
                        branch=branch,
                        reason='purchase',
                        quantity_change=10,
                        note='Initial stock setup on product creation',
                        performed_by=request.user
                    )'''

replace_add = r'''            skus = request.POST.getlist('sku[]')
            if not skus:  # fallback
                skus = [request.POST.get('sku', '')]
            cost_prices = request.POST.getlist('cost_price[]') or [request.POST.get('cost_price', 0)]
            selling_prices = request.POST.getlist('selling_price[]') or [request.POST.get('selling_price', 0)]
            discount_prices = request.POST.getlist('discount_price[]') or [request.POST.get('discount_price', '')]
            attr_models = request.POST.getlist('attr_model[]') or [request.POST.get('attr_model', '')]
            attr_variants = request.POST.getlist('attr_variant[]') or [request.POST.get('attr_variant', '')]
            
            with transaction.atomic():
                category = get_object_or_404(Category, store=request.store, id=category_id)
                brand = Brand.objects.filter(store=request.store, id=brand_id).first() if brand_id else None
                
                product = Product.objects.create(
                    store=request.store,
                    category=category,
                    brand=brand,
                    name=name,
                    description=description,
                    tags=tags,
                    status='active'
                )
                
                for i in range(len(skus)):
                    v_sku = skus[i].strip()
                    if not v_sku: continue
                    v_cost = float(cost_prices[i] or 0) if i < len(cost_prices) else 0.0
                    v_sell = float(selling_prices[i] or 0) if i < len(selling_prices) else 0.0
                    v_disc_raw = discount_prices[i] if i < len(discount_prices) else ''
                    v_disc = float(v_disc_raw) if v_disc_raw else None
                    
                    attributes = {}
                    if i < len(attr_models) and attr_models[i].strip():
                        attributes['Model'] = attr_models[i].strip()
                    if i < len(attr_variants) and attr_variants[i].strip():
                        attributes['Variant'] = attr_variants[i].strip()
                        
                    variant = ProductVariant.objects.create(
                        store=request.store,
                        product=product,
                        sku=v_sku,
                        cost_price=v_cost,
                        selling_price=v_sell,
                        discount_price=v_disc,
                        attributes=attributes,
                        is_active=True
                    )
                    
                    if i == 0:
                        branch = Branch.objects.filter(store=request.store, is_default=True).first() or Branch.objects.filter(store=request.store).first()
                        if branch:
                            Stock.objects.create(store=request.store, variant=variant, branch=branch, quantity=10, low_stock_threshold=5)
                            StockMovement.objects.create(store=request.store, variant=variant, branch=branch, reason='purchase', quantity_change=10, note='Initial stock setup', performed_by=request.user)
                
                if images:
                    for idx, img in enumerate(images):
                        ProductImage.objects.create(store=request.store, product=product, image=img, is_primary=(idx == 0), order=idx + 1)'''

text = text.replace(search_add, replace_add)

# Replace edit_product variant logic
search_edit = r'''            attributes = {}
            attr_model = request.POST.get('attr_model', '').strip()
            attr_variant = request.POST.get('attr_variant', '').strip()
            if attr_model:
                attributes['Model'] = attr_model
            if attr_variant:
                attributes['Variant'] = attr_variant
            
            with transaction.atomic():
                product = get_object_or_404(Product, store=request.store, id=product_id)
                category = get_object_or_404(Category, store=request.store, id=category_id)
                brand = Brand.objects.filter(store=request.store, id=brand_id).first() if brand_id else None
                
                product.category = category
                product.brand = brand
                product.name = name
                product.description = description
                product.tags = tags
                product.save()
                
                variant = product.variants.first()
                if variant:
                    variant.sku = sku
                    variant.cost_price = cost_price
                    variant.selling_price = selling_price
                    variant.discount_price = discount_price
                    variant.attributes = attributes
                    variant.save()
                    
                if images:
                    ProductImage.objects.filter(product=product).delete()
                    for idx, img in enumerate(images):
                        ProductImage.objects.create(
                            store=request.store,
                            product=product,
                            image=img,
                            is_primary=(idx == 0),
                            order=idx + 1
                        )'''

replace_edit = r'''            variant_ids = request.POST.getlist('variant_id[]')
            skus = request.POST.getlist('sku[]')
            if not skus:
                skus = [request.POST.get('sku', '')]
            cost_prices = request.POST.getlist('cost_price[]') or [request.POST.get('cost_price', 0)]
            selling_prices = request.POST.getlist('selling_price[]') or [request.POST.get('selling_price', 0)]
            discount_prices = request.POST.getlist('discount_price[]') or [request.POST.get('discount_price', '')]
            attr_models = request.POST.getlist('attr_model[]') or [request.POST.get('attr_model', '')]
            attr_variants = request.POST.getlist('attr_variant[]') or [request.POST.get('attr_variant', '')]
            
            with transaction.atomic():
                product = get_object_or_404(Product, store=request.store, id=product_id)
                category = get_object_or_404(Category, store=request.store, id=category_id)
                brand = Brand.objects.filter(store=request.store, id=brand_id).first() if brand_id else None
                
                product.category = category
                product.brand = brand
                product.name = name
                product.description = description
                product.tags = tags
                product.save()
                
                submitted_variant_ids = [int(v) for v in variant_ids if v.strip().isdigit()]
                
                for v in product.variants.all():
                    if v.id not in submitted_variant_ids:
                        try:
                            v.delete()
                        except:
                            v.is_active = False
                            v.save()
                            
                for i in range(len(skus)):
                    v_sku = skus[i].strip()
                    if not v_sku: continue
                    v_cost = float(cost_prices[i] or 0) if i < len(cost_prices) else 0.0
                    v_sell = float(selling_prices[i] or 0) if i < len(selling_prices) else 0.0
                    v_disc_raw = discount_prices[i] if i < len(discount_prices) else ''
                    v_disc = float(v_disc_raw) if v_disc_raw else None
                    v_id_str = variant_ids[i] if i < len(variant_ids) else ''
                    
                    attributes = {}
                    if i < len(attr_models) and attr_models[i].strip():
                        attributes['Model'] = attr_models[i].strip()
                    if i < len(attr_variants) and attr_variants[i].strip():
                        attributes['Variant'] = attr_variants[i].strip()
                        
                    if v_id_str.strip().isdigit():
                        v_id = int(v_id_str)
                        variant = ProductVariant.objects.get(id=v_id, product=product)
                        variant.sku = v_sku
                        variant.cost_price = v_cost
                        variant.selling_price = v_sell
                        variant.discount_price = v_disc
                        variant.attributes = attributes
                        variant.is_active = True
                        variant.save()
                    else:
                        variant = ProductVariant.objects.create(
                            store=request.store,
                            product=product,
                            sku=v_sku,
                            cost_price=v_cost,
                            selling_price=v_sell,
                            discount_price=v_disc,
                            attributes=attributes,
                            is_active=True
                        )
                        branch = Branch.objects.filter(store=request.store, is_default=True).first() or Branch.objects.filter(store=request.store).first()
                        if branch:
                            Stock.objects.create(store=request.store, variant=variant, branch=branch, quantity=10, low_stock_threshold=5)
                            StockMovement.objects.create(store=request.store, variant=variant, branch=branch, reason='purchase', quantity_change=10, note='Initial stock setup', performed_by=request.user)

                if images:
                    ProductImage.objects.filter(product=product).delete()
                    for idx, img in enumerate(images):
                        ProductImage.objects.create(store=request.store, product=product, image=img, is_primary=(idx == 0), order=idx + 1)'''

text = text.replace(search_edit, replace_edit)

with open(views_file, 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
