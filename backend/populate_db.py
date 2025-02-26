from pymongo import MongoClient
from bson.objectid import ObjectId
import random

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["meubanco"]
products_collection = db["products"]
categories_collection = db["categories"]
orders_collection = db["orders"]

# Dados fictícios
categories = [
    {"name": "Eletrônicos", "description": "Celulares, laptops e gadgets."},
    {"name": "Roupas", "description": "Moda masculina e feminina."},
    {"name": "Livros", "description": "Livros de diversos gêneros."},
    {"name": "Alimentos", "description": "Comida e bebidas."}
]

products = [
    {"name": "iPhone 13", "description": "Smartphone da Apple", "price": 6999.99},
    {"name": "Notebook Dell", "description": "Laptop para trabalho", "price": 4999.99},
    {"name": "Camisa Polo", "description": "Camisa de algodão", "price": 99.99},
    {"name": "Livro Python", "description": "Aprenda Python", "price": 59.99},
    {"name": "Chocolate", "description": "Chocolate ao leite", "price": 10.99}
]

# Inserir categorias
category_ids = []
for category in categories:
    result = categories_collection.insert_one(category)
    category_ids.append(result.inserted_id)

# Inserir produtos associando a uma categoria
for product in products:
    product["category_id"] = random.choice(category_ids)  # Relaciona com uma categoria aleatória
    products_collection.insert_one(product)

# Criar pedidos fictícios
for _ in range(5):
    sample_products = list(products_collection.aggregate([{ "$sample": { "size": 3 } }]))
    total_price = sum(p["price"] for p in sample_products)
    orders_collection.insert_one({
        "products": [str(p["_id"]) for p in sample_products],
        "total": total_price
    })

print("Banco de dados populado com sucesso!")
