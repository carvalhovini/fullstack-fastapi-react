from fastapi import FastAPI, HTTPException
from app.database import db
from app.models import Product, Category, Order

app = FastAPI()

# Criar um produto
@app.post("/products/")
def create_product(product: Product):
    result = db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

# Listar produtos
@app.get("/products/")
def list_products():
    return list(db.products.find({}, {"_id": 0}))

# Criar categoria
@app.post("/categories/")
def create_category(category: Category):
    result = db.categories.insert_one(category.dict())
    return {"id": str(result.inserted_id)}

# Criar pedido
@app.post("/orders/")
def create_order(order: Order):
    result = db.orders.insert_one(order.dict())
    return {"id": str(result.inserted_id)}
