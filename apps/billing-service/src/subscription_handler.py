"""
Subscription charge handling. PCI scope — no raw card data in logs, ever.
Reviewed by @identitysec/security on every change per CONTRIBUTING.md.
"""
from platform_packages.logger import get_logger

log = get_logger(__name__)


def process_subscription_charge(customer_id: str, amount_cents: int, payment_token: str) -> dict:
    """payment_token is a tokenized reference from the PSP, never a raw card number."""
    log.info(f"processing subscription charge for customer={customer_id} amount_cents={amount_cents}")
    return {"status": "succeeded", "customer_id": customer_id}
