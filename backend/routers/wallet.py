from fastapi import APIRouter, Depends, HTTPException
import crud
import schemas
from database import async_sessionmaker, AsyncSession, get_db
router=APIRouter(prefix='/wallet')


@router.get('/{user_id}/balance')
async def get_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user.id,
        "balance": user.balance,
        "last_updated": user.updated_at
    }





@router.post('/{user_id}/add-money')
async def add_money(user_id: int, transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_balance = user.balance + transaction.amount
    user.balance = new_balance
    await db.commit()
    await db.refresh(user)

    return {
        "transaction_id": 123,
        "user_id": user.id,
        "amount": transaction.amount,
        "new_balance": new_balance,
        "transaction_type": "CREDIT"
    }


@router.post('/{user_id}/withdraw')
async def withdraw_money(user_id: int, transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance -= transaction.amount
    await db.commit()
    await db.refresh(user)

    return {
        "transaction_id": 123,
        "user_id": user.id,
        "amount": transaction.amount,
        "new_balance": user.balance,
        "transaction_type": "DEBIT"
    }
