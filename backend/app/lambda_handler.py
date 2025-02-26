from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

def process_orders(event, context):
    """ Função Lambda para processar relatórios de vendas """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    total_orders = db.orders.count_documents({})
    total_value = sum(order['total'] for order in db.orders.find({}))
    avg_value = total_value / total_orders if total_orders > 0 else 0

    report = {
        "total_orders": total_orders,
        "total_value": total_value,
        "avg_value": avg_value
    }

    return {
        "statusCode": 200,
        "body": report
    }