from fastapi import FastAPI, HTTPException

STUDENT_N = 6

app = FastAPI(title=f"Product Service N{STUDENT_N}")

# База даних товарів на складі (ID починаються з 600)
PRODUCTS = {
    STUDENT_N * 100 + 1: {"id": STUDENT_N * 100 + 1, "name": "Ноутбук Dell", "price": 1200.0, "stock": 5},
    STUDENT_N * 100 + 2: {"id": STUDENT_N * 100 + 2, "name": "Мишка Logitech", "price": 25.0, "stock": 50},
    STUDENT_N * 100 + 3: {"id": STUDENT_N * 100 + 3, "name": "Клавіатура Keychron", "price": 100.0, "stock": 0}
}

@app.get("/products")
def get_all_products():
    """Повертає список усіх доступних товарів"""
    return {"student_id": STUDENT_N, "products": list(PRODUCTS.values())}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Повертає інформацію про конкретний товар за ID"""
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"student_id": STUDENT_N, "data": PRODUCTS[product_id]}
