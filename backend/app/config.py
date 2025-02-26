import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "fullstack_db")