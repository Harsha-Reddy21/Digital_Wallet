
from fastapi import APIRouter, Depends, HTTPException

import crud
import schemas
from database import async_sessionmaker, AsyncSession, get_db


router = APIRouter(prefix='/users')


@router.get('/{user_id}')
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_details={
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "balance": user.balance,
        "created_at": user.created_at
    }
    return user_details


@router.post('/')
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db=db, user=user)
    return {"user_id": db_user.id}