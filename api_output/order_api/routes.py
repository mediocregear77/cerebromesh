# File: api_output/order_api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Schema definitions
class Order(BaseModel):
    order_id: int
    user_id: int
    items: List[str]
    status: str

class CreateOrderRequest(BaseModel):
    user_id: int
    items: List[str]

# Dummy storage
orders_db = []

# Endpoints
@router.post("/orders", response_model=Order)
async def create_order(order_request: CreateOrderRequest):
    new_order = Order(
        order_id=len(orders_db) + 1,
        user_id=order_request.user_id,
        items=order_request.items,
        status="pending"
    )
    orders_db.append(new_order)
    return new_order

@router.get("/orders", response_model=List[Order])
async def get_all_orders():
    return orders_db

@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    for order in orders_db:
        if order.order_id == order_id:
            return order
    return {"error": "Order not found"}
