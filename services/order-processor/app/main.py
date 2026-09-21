from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Processor")


class Order(BaseModel):
    order_id: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/process")
def process_order(order: Order):
    return {
        "order_id": order.order_id,
        "status": "PROCESSED"
    }