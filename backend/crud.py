
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




async def create_transaction(db:AsyncSession, transaction:schemas.TransactionCreate, transaction_type: str = None):
    data = transaction.dict() 
    if transaction_type:
        data["transaction_type"] = transaction_type
    db_transaction = models.Transaction(**data)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def create_transfer_transaction(db: AsyncSession, transaction: schemas.TransferTransactionCreate):
    """Create a transaction with all transfer-specific fields"""
    data = transaction.dict()
    db_transaction = models.Transaction(**data)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def count_user_transactions(db: AsyncSession, user_id: int):
    """Count total transactions for a user"""
    result = await db.execute(select(func.count(models.Transaction.id)).where(models.Transaction.user_id == user_id))
    return result.scalar()

async def get_transfer(db: AsyncSession, transfer_id: str):
    """Get transfer details by transfer_id (placeholder implementation)"""
    # This would need a Transfer model or a way to identify transfers
    # For now, return None as this functionality needs to be designed
    return None