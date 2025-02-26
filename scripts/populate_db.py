from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Dados fictícios
categories = [
    {"name": "Eletrônicos"},
    {"name": "Roupas"},
    {"name": "Livros"}
]

products = [
    {"name": "Celular", "description": "Smartphone com 128GB", "price": 2000.00, "category_ids": []},
    {"name": "Notebook", "description": "Laptop i7 com 16GB RAM", "price": 4500.00, "category_ids": []},
    {"name": "Camisa", "description": "Camisa de algodão tamanho M", "price": 80.00, "category_ids": []},
]

# Inserir dados
category_ids = db.categories.insert_many(categories).inserted_ids
for i, product in enumerate(products):
    product["category_ids"] = [str(category_ids[i % len(category_ids)])]

db.products.insert_many(products)

print("Banco de dados populado com sucesso!")