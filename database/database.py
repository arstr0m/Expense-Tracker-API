from motor.motor_asyncio import AsyncIOMotorClient

from consts.consts import get_host


def get_client():
    client = AsyncIOMotorClient(get_host())
    return client


def get_db():
    client = get_client()
    db = client.expense_tracker_api
    return db


def get_collection(name):
    db = get_db()
    collection = db[name]
    return collection

