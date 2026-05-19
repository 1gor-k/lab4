from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

STUDENT_N = 6

app = FastAPI(title=f"Order Service N{STUDENT_N}")

PRODUCT_SERVICE_URL = "http://product-service-06:8000"

class OrderRequest(BaseModel):
    product_id: int
    quantity: int

ORDERS = []

@app.post("/orders")
def create_order(order: OrderRequest):
    """Створює замовлення, попередньо перевіряючи наявність товару на складі"""
    # 1. Запит до першого мікросервісу
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{order.product_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Product Service is unavailable")

    # 2. Перевірка чи існує такий товар
    if response.status_code == 404:
        raise HTTPException(status_code=400, detail="Product does not exist on warehouse")

    product_data = response.json()["data"]

    # 3. Перевірка наявності на складі
    if product_data["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock for this product")

    # 4. Збереження замовлення
    new_order = {
        "order_id": len(ORDERS) + 1,
        "product_id": order.product_id,
        "product_name": product_data["name"],
        "quantity": order.quantity,
        "total_price": product_data["price"] * order.quantity,
        "status": "Shipped",
        "student_id": STUDENT_N
    }
    ORDERS.append(new_order)
    return new_order

@app.get("/orders")
def get_all_orders():
    """Повертає список усіх відвантажень"""
    return {"student_id": STUDENT_N, "orders": ORDERS}
