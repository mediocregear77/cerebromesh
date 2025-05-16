# File: marketplace/monetization.py

import stripe
from typing import Dict, Any

# ⚠️ Replace with your real Stripe test key or environment secret
stripe.api_key = "sk_test_your_test_key_here"

class MonetizationEngine:
    def __init__(self):
        self.currency = "usd"

    def create_product(self, name: str, description: str) -> Dict[str, Any]:
        product = stripe.Product.create(name=name, description=description)
        return product

    def create_price(self, product_id: str, unit_amount: int) -> Dict[str, Any]:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=self.currency
        )
        return price

    def create_checkout_session(self, price_id: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session

    def generate_purchase_link(self, name: str, description: str, price_dollars: float, success_url: str, cancel_url: str) -> str:
        product = self.create_product(name, description)
        price_cents = int(price_dollars * 100)
        price = self.create_price(product.id, price_cents)
        session = self.create_checkout_session(price.id, success_url, cancel_url)
        return session.url
