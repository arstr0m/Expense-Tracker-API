# crud.py
from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import Depends, HTTPException
from pymongo import collection

from auth.auth import get_current_user
from auth.security import hash_password

from database.database import get_collection
from schemas.schemas import UserCreate, ExpenseCreate


async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict['password'] = hash_password(user_dict['password'])
    result = await get_collection('users').insert_one(user_dict)
    return str(result.inserted_id)


async def get_user(email: str):
    user = await get_collection('users').find_one({"email": email})
    return user


async def create_expense(expense: ExpenseCreate):
    expense_dict = expense.dict()
    expense_dict['date'] = datetime.strptime(expense_dict['date'], '%Y-%m-%d')
    result = await get_collection('expenses').insert_one(expense_dict)
    return str(result.inserted_id)


async def get_all_expenses_from_db(current_user: str):
    collection = get_collection('expenses')
    query = {"user_email": current_user}
    cursor = collection.find(query)
    expenses = await cursor.to_list(length=100)
    for expense in expenses:
        expense["id"] = str(expense["_id"])
        if "date" in expense:
            expense["date"] = expense["date"].isoformat()
        del expense["_id"]
    return expenses


async def get_by_category(current_user: str, category: str):
    collection = get_collection('expenses')
    query = {"user_email": current_user, "category": category}
    cursor = collection.find(query)
    expenses = await cursor.to_list(length=100)
    for expense in expenses:
        expense["id"] = str(expense["_id"])
        if "date" in expense:
            expense["date"] = expense["date"].isoformat()
        del expense["_id"]
    return expenses


def calculate_date_range(category: str, start_date: str = None, end_date: str = None):
    now = datetime.now()
    if category == "past_week":
        start_date = (now - timedelta(weeks=1)).isoformat()
        end_date = now.isoformat()
    elif category == "last_month":
        start_date = (now - timedelta(days=30)).isoformat()
        end_date = now.isoformat()
    elif category == "last_3_months":
        start_date = (now - timedelta(days=90)).isoformat()
        end_date = now.isoformat()
    elif category == "custom":
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').isoformat()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').isoformat()
        else:
            raise ValueError("Start date and end date must be provided for custom filter")
    else:
        raise ValueError("Invalid filter type")
    return start_date, end_date


async def get_expenses(filter, token: str) -> list:
    collection = get_collection('expenses')
    query = {"user_email": token}

    if filter.category:
        query["category"] = filter.category

    try:
        start_date, end_date = calculate_date_range(
            filter.mode,
            filter.start_date,
            filter.end_date
        )
        query["date"] = {
            "$gte": datetime.fromisoformat(start_date),
            "$lte": datetime.fromisoformat(end_date)
        }
    except Exception as e:
        HTTPException(status_code=400, detail=str(e))

    cursor = collection.find(query)
    expenses = await cursor.to_list(length=100)

    for expense in expenses:
        expense["id"] = str(expense["_id"])
        if "date" in expense:
            expense["date"] = expense["date"].isoformat()
        del expense["_id"]

    return expenses


async def delete_expense(expense_id: str):
    result = await get_collection('expenses').delete_one({"_id": ObjectId(expense_id)})
    return result.deleted_count


async def update_expense(expense_id: str, expense_data: dict):
    result = await get_collection('expenses').update_one({"_id": ObjectId(expense_id)}, {"$set": expense_data})
    return result.modified_count
