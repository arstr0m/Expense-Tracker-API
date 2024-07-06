from auth.auth import get_current_user
from database.cache import get_data, set_data
from database.crud import delete_expense, get_expenses, create_expense, get_all_expenses_from_db, get_by_category
from fastapi import APIRouter, HTTPException, Depends

from models.models import TokenData, GetExpense
from schemas.schemas import ExpenseFilter, ExpenseCreate, ExpenseResponse

router_expenses = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
    responses={404: {"description": "Not found"}},
)


@router_expenses.post("/", response_model=str)
async def add_expense(expense: ExpenseCreate, token: TokenData = Depends(get_current_user)):
    expense.user_email = token
    expense = await create_expense(expense)
    return expense


@router_expenses.get("/all/{category}", response_model=list[GetExpense])
async def get_expense_by_category(category: str, token: str = Depends(get_current_user)):
    cache_key = f"expenses_all:{token}:{category}"
    cached_data = get_data(cache_key)
    if cached_data:
        return cached_data
    expenses = await get_by_category(token, category)
    if expenses is None:
        raise HTTPException(status_code=404, detail="No expenses found")
    set_data(cache_key, expenses, expiration=300)
    return expenses


@router_expenses.get("/all", response_model=list[ExpenseResponse])
async def get_all_expenses(token: str = Depends(get_current_user)):
    cache_key = f"expenses_all:{token}:all"
    cached_data = get_data(cache_key)
    if cached_data:
        return cached_data
    expenses = await get_all_expenses_from_db(token)
    if expenses is None:
        raise HTTPException(status_code=404, detail="No expenses found")
    set_data(cache_key, expenses, expiration=300)
    return expenses


@router_expenses.get("/", response_model=list[ExpenseResponse])
async def list_expenses(filter: ExpenseFilter = Depends(), token: str = Depends(get_current_user)):
    cache_key = f"expenses_all:{token}:get"
    cached_data = get_data(cache_key)
    if cached_data:
        return cached_data
    expenses = await get_expenses(filter, token)
    if expenses is None:
        raise HTTPException(status_code=404, detail="No expenses found")
    set_data(cache_key, expenses, expiration=300)
    return expenses


@router_expenses.delete("/{expense_id}", response_model=int)
async def remove_expense(expense_id: str, token: str = Depends(get_current_user)):
    result = await delete_expense(expense_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result


@router_expenses.put("/{expense_id}", response_model=int)
async def update_expense(expense_id: str, expense: ExpenseCreate, token: str = Depends(get_current_user)):
    result = await update_expense(expense_id, expense.dict())
    if result == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result
