
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





async def get_transactions(db:AsyncSession, user_id:int, page:int=1, limit:int=10):
    offset = (page - 1) * limit
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id).offset(offset).limit(limit))
    return result.scalars().all()




async def get_transaction(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(models.Transaction).where(models.Transaction.id == transaction_id))
    return result.scalar_one_or_none()




async def create_transaction(db:AsyncSession, transaction:schemas.TransactionCreate,transaction_type=None):
    data=transaction.dict() 
    data["transaction_type"] = transaction_type
    db_transaction = models.Transaction(**data)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction