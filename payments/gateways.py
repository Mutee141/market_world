from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    """
    Every gateway (JazzCash, EasyPaisa, future ones) implements this same
    interface. Views/services call gateways ONLY through this interface —
    never call a specific gateway's SDK directly outside its own class.
    """

    @abstractmethod
    def initiate_payment(self, payment, return_url: str) -> dict:
        """Starts a payment. Returns dict with at least {'redirect_url': ...} or
        {'requires_otp': True, ...} depending on gateway flow."""
        raise NotImplementedError

    @abstractmethod
    def verify_payment(self, payment, callback_data: dict) -> bool:
        """Verifies a callback/webhook from the gateway. Returns True if payment
        is confirmed successful, and should update payment.status/paid_at itself."""
        raise NotImplementedError


class JazzCashGateway(PaymentGateway):
    """
    Real integration needs your JazzCash merchant credentials (merchant ID,
    password, integrity salt) from their merchant portal — placeholders below.
    Docs: JazzCash Mobile Account / Card API (HTTPS POST with hash-secured
    fields). We'll wire in real credentials + the hash-generation logic once
    you have your merchant account approved.
    """

    def initiate_payment(self, payment, return_url: str) -> dict:
        # TODO: build the pp_ fields payload + secure hash, POST to JazzCash sandbox/live URL
        return {
            'redirect_url': f'https://sandbox.jazzcash.com.pk/pay?ref={payment.id}',
            'status': 'redirect_required',
        }

    def verify_payment(self, payment, callback_data: dict) -> bool:
        # TODO: validate secure hash from callback_data against your integrity salt
        success = callback_data.get('pp_ResponseCode') == '000'
        if success:
            from django.utils import timezone
            payment.status = 'paid'
            payment.transaction_id = callback_data.get('pp_TxnRefNo')
            payment.gateway_response = callback_data
            payment.paid_at = timezone.now()
            payment.save()
        else:
            payment.status = 'failed'
            payment.gateway_response = callback_data
            payment.save()
        return success


class EasyPaisaGateway(PaymentGateway):
    """Same pattern as JazzCash — needs EasyPaisa merchant credentials to go live."""

    def initiate_payment(self, payment, return_url: str) -> dict:
        return {
            'redirect_url': f'https://easypaisa.com.pk/pay?ref={payment.id}',
            'status': 'redirect_required',
        }

    def verify_payment(self, payment, callback_data: dict) -> bool:
        success = callback_data.get('status') == 'success'
        if success:
            from django.utils import timezone
            payment.status = 'paid'
            payment.transaction_id = callback_data.get('transactionId')
            payment.gateway_response = callback_data
            payment.paid_at = timezone.now()
            payment.save()
        else:
            payment.status = 'failed'
            payment.gateway_response = callback_data
            payment.save()
        return success


class CashGateway(PaymentGateway):
    """Used for COD and in-store cash — no external call, just marks paid immediately (POS) or on delivery (COD)."""

    def initiate_payment(self, payment, return_url: str) -> dict:
        payment.status = 'paid' if payment.method == 'cash' else 'pending'
        if payment.status == 'paid':
            from django.utils import timezone
            payment.paid_at = timezone.now()
        payment.save()
        return {'status': payment.status}

    def verify_payment(self, payment, callback_data: dict) -> bool:
        return payment.status == 'paid'


GATEWAY_MAP = {
    'jazzcash': JazzCashGateway,
    'easypaisa': EasyPaisaGateway,
    'cash': CashGateway,
    'cod': CashGateway,
}


def get_gateway(method: str) -> PaymentGateway:
    gateway_class = GATEWAY_MAP.get(method)
    if not gateway_class:
        raise ValueError(f"No gateway configured for payment method '{method}'")
    return gateway_class()