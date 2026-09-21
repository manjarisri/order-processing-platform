from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")


class Notification(BaseModel):
    order_id: str
    message: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/notify")
def notify(notification: Notification):
    print(
        f"Notification for {notification.order_id}: "
        f"{notification.message}"
    )

    return {
        "order_id": notification.order_id,
        "status": "NOTIFICATION_SENT",
        "message": notification.message
    }