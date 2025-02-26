from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: str
    price: float
    category_ids: List[str]
    image_url: str

class Category(BaseModel):
    id: Optional[str]
    name: str

class Order(BaseModel):
    id: Optional[str]
    date: datetime
    product_ids: List[str]
    total: float
