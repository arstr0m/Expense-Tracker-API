# schemas.py
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    email: str


class ExpenseCreate(BaseModel):
    category: str
    amount: float
    date: str
    description: Optional[str] = None
    user_email: Optional[str] = None


class ExpenseResponse(BaseModel):
    category: str
    amount: float
    date: str
    description: Optional[str] = None


class ExpenseFilter(BaseModel):
    mode: Optional[str] = None
    category: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None



