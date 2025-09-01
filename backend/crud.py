
from database import Base, get_db, AsyncSession
from fastapi import Depends
from sqlalchemy import func, select

import models
import schemas


async def get_user(db:AsyncSession, user_id:int=None):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def create_user(db:AsyncSession, user:schemas.UserCreate):
    print(user)
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db:AsyncSession, user_id:int, user:schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user is None:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user



async def get_transactions(db:AsyncSession, user_id:int, page:int=1, limit:int=10):
    offset = (page - 1) * limit
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id).offset(offset).limit(limit))
    return result.scalars().all()




async def get_transaction(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(models.Transaction).where(models.Transaction.id == transaction_id))
    return result.scalar_one_or_none()




async def create_transaction(db:AsyncSession, transaction:schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction