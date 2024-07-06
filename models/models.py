from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True


class Expense(BaseModel):
    category: str
    amount: float
    date: str
    description: Optional[str] = None
    user_email: Optional[str] = None


class GetExpense(BaseModel):
    category: str
    amount: float
    date: datetime
    description: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
