from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List
import boto3
from fastapi import APIRouter
from datetime import datetime, timedelta

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["meubanco"]
products_collection = db["products"]
categories_collection = db["categories"]
orders_collection = db["orders"]

# Configurando o LocalStack (simulando AWS S3)
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

BUCKET_NAME = "produtos-bucket"
s3.create_bucket(Bucket=BUCKET_NAME)  # Criar bucket no LocalStack

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_key = f"images/{file.filename}"
        
        # Upload para o S3 (com logs ativados)
        s3.upload_fileobj(file.file, BUCKET_NAME, file_key)

        image_url = f"http://localhost:4566/{BUCKET_NAME}/{file_key}"
        return {"image_url": image_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

# 📌 Modelo de Categoria
class Category(BaseModel):
    name: str
    description: Optional[str] = None

# 📌 Modelo de Produto (agora com imagem e categoria)
class Product(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[str] = None
    image_url: Optional[str] = None  # Suporte a upload de imagens

# 📌 Modelo de Pedido
class Order(BaseModel):
    products: List[dict]  # Deve armazenar lista de produtos com nome e preço
    total: Optional[float] = 0.0  # O total será calculado automaticamente

### 📌 CRUD de Categorias ###
@app.post("/categories/")
async def create_category(category: Category):
    category_dict = category.dict()
    result = categories_collection.insert_one(category_dict)
    category_dict["_id"] = str(result.inserted_id)
    return category_dict

@app.get("/categories/")
async def get_categories():
    categories = list(categories_collection.find({}))
    for category in categories:
        category["_id"] = str(category["_id"])
    return categories

@app.put("/categories/{category_id}")
async def update_category(category_id: str, category: Category):
    updated_category = categories_collection.find_one_and_update(
        {"_id": ObjectId(category_id)},
        {"$set": category.dict()},
        return_document=True
    )
    if updated_category:
        updated_category["_id"] = str(updated_category["_id"])
        return updated_category
    raise HTTPException(status_code=404, detail="Categoria não encontrada")

@app.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count:
        return {"message": "Categoria deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Categoria não encontrada")

### 📌 CRUD de Produtos ###
@app.post("/products/")
async def create_product(product: Product):
    product_dict = product.dict()

    if product.category_id:
        category = categories_collection.find_one({"_id": ObjectId(product.category_id)})
        if not category:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")

    result = products_collection.insert_one(product_dict)
    product_dict["_id"] = str(result.inserted_id)
    return product_dict

@app.get("/products/")
async def get_products():
    products = list(products_collection.find({}))
    for product in products:
        product["_id"] = str(product["_id"])

        if "category_id" in product and product["category_id"]:
            category = categories_collection.find_one({"_id": ObjectId(product["category_id"])})
            product["category_name"] = category["name"] if category else "Categoria não encontrada"

    return products

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    try:
        obj_id = ObjectId(product_id)
        result = products_collection.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao excluir produto: {str(e)}")

### 📌 CRUD de Pedidos ###
@app.post("/orders/")
async def create_order(order: dict):
    try:
        if not order["products"]:
            raise HTTPException(status_code=400, detail="O pedido deve conter ao menos um produto.")

        total_price = 0
        product_list = []

        for product_id in order["products"]:
            product = products_collection.find_one({"_id": ObjectId(product_id)})
            if not product:
                raise HTTPException(status_code=404, detail=f"Produto com ID {product_id} não encontrado.")
            product_list.append(product_id)
            total_price += product["price"]  # Somando os preços corretamente

        order_dict = {
            "products": product_list,
            "total": total_price,  # ✅ Agora está correto!
            "created_at": datetime.utcnow()  # Adiciona timestamp
        }

        result = orders_collection.insert_one(order_dict)
        order_dict["_id"] = str(result.inserted_id)

        return order_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")


@app.get("/orders/")
async def get_orders():
    orders = list(orders_collection.find({}))
    for order in orders:
        order["_id"] = str(order["_id"])
    return orders

@app.put("/orders/{order_id}")
async def update_order(order_id: str, order: Order):
    updated_order = orders_collection.find_one_and_update(
        {"_id": ObjectId(order_id)},
        {"$set": order.dict()},
        return_document=True
    )
    if updated_order:
        updated_order["_id"] = str(updated_order["_id"])
        return updated_order
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    result = orders_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count:
        return {"message": "Pedido deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


router = APIRouter()

# 📌 Nova rota para calcular KPIs 📊
@app.get("/kpis/")
async def get_kpis():
    try:
        total_pedidos = orders_collection.count_documents({})

        total_receita = sum(
            order["total"] for order in orders_collection.find({}) if "total" in order
        )

        media_pedido = total_receita / total_pedidos if total_pedidos > 0 else 0

        # 📌 Pedidos por período
        today = datetime.utcnow()
        start_of_week = today - timedelta(days=today.weekday())  # Segunda-feira
        start_of_month = today.replace(day=1)

        pedidos_hoje = orders_collection.count_documents(
            {"created_at": {"$gte": today.replace(hour=0, minute=0, second=0, microsecond=0)}}
        )

        pedidos_semana = orders_collection.count_documents(
            {"created_at": {"$gte": start_of_week}}
        )

        pedidos_mes = orders_collection.count_documents(
            {"created_at": {"$gte": start_of_month}}
        )

        return {
            "total_pedidos": total_pedidos,
            "total_receita": total_receita,
            "media_pedido": media_pedido,
            "pedidos_hoje": pedidos_hoje,
            "pedidos_semana": pedidos_semana,
            "pedidos_mes": pedidos_mes,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular KPIs: {str(e)}")
