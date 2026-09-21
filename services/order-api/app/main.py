from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4

app = FastAPI(title="Order API")


# In-memory storage for demo purposes
orders: Dict[str, dict] = {}


class OrderRequest(BaseModel):
    product: str
    quantity: int


class OrderResponse(BaseModel):
    order_id: str
    product: str
    quantity: int
    status: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "order-api"
    }


@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderRequest):

    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    order_id = f"ORD-{uuid4().hex[:8].upper()}"

    new_order = {
        "order_id": order_id,
        "product": order.product,
        "quantity": order.quantity,
        "status": "CREATED"
    }

    orders[order_id] = new_order

    return new_order


@app.get("/orders/{order_id}")
def get_order(order_id: str):

    if order_id not in orders:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return orders[order_id]