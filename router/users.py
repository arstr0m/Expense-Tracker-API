from fastapi import APIRouter, HTTPException, Depends

from auth.auth import create_access_token, get_current_user
from database.crud import create_user, get_user
from models.models import Token
from schemas.schemas import UserCreate

router_users = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router_users.get("/me", response_model=Token)
async def get_me(token: str = Depends(get_current_user)):
    return {"access_token": token, "token_type": "bearer"}


@router_users.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await get_user(user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router_users.post('/signup')
async def register(user: UserCreate):
    db_user = await get_user(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    await create_user(user)
    print(user.email)
    access_token = create_access_token(data={"sub": user.email})
    return {"message": "User created", "access_token": access_token, "token_type": "bearer"}
