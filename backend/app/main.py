from fastapi import FastAPI
from app.routes import app as routes_app

app = FastAPI()

app.include_router(routes_app)

@app.get("/")
def home():
    return {"message": "API is running"}
