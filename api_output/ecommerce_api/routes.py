# File: api_output/ecommerce_api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Sample schema models
class Product(BaseModel):
    id: int
    name: str
    price: float

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CheckoutPayload(BaseModel):
    items: List[CartItem]
    user_id: int
    payment_method: str

# Endpoints
@router.get("/products", response_model=List[Product])
async def get_products():
    return [
        {"id": 1, "name": "T-Shirt", "price": 19.99},
        {"id": 2, "name": "Sneakers", "price": 79.95},
    ]

@router.post("/cart")
async def add_to_cart(item: CartItem):
    return {"message": "Item added to cart", "item": item}

@router.post("/checkout")
async def process_checkout(payload: CheckoutPayload):
    return {
        "message": "Checkout complete",
        "user_id": payload.user_id,
        "total_items": len(payload.items),
    }
