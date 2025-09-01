


from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import TransactionCreate
from database import async_sessionmaker, AsyncSession, get_db
import crud
router = APIRouter(prefix='/transactions')


@router.get('/{user_id}')
async def get_transactions(user_id: int, page: int = Query(1), limit: int = Query(10), db: AsyncSession = Depends(get_db)):
    transactions = await crud.get_transactions(db=db, user_id=user_id, page=page, limit=limit)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")

    total = await crud.count_user_transactions(db=db, user_id=user_id)
    return {
        "transactions": transactions,
        "total": total,
        "page": page,
        "limit": limit
    }




@router.get('/detail/{transaction_id}')
async def get_transaction_detail(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await crud.get_transaction(db=db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "transaction_id": transaction.id,
        "user_id": transaction.user_id,
        "transaction_type": transaction.transaction_type,
        "amount": transaction.amount,
        "description": transaction.description,
        "recipient_user_id": transaction.recipient_user_id,
        "reference_transaction_id": transaction.reference_transaction_id,
        "created_at": transaction.created_at
    }


@router.post('/')
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    db_transaction = await crud.create_transaction(db=db, transaction=transaction)
    return {"transaction_id": db_transaction.id}
