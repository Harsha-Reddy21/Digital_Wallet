

from fastapi import APIRouter, Depends, HTTPException
import schemas
from schemas import  TransactionCreate, TransferCreate
from database import async_sessionmaker, AsyncSession, get_db
import crud

router = APIRouter(prefix='/transfers')



@router.get('/{transfer_id}')
async def get_transfer(transfer_id: str, db: AsyncSession = Depends(get_db)):
    transfer = await crud.get_transfer(db=db, transfer_id=transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer




# POST /transfer
# Request Body:
# {
#   "sender_user_id": 1,
#   "recipient_user_id": 2,
#   "amount": 25.00,
#   "description": "Payment for dinner"
# }
# Response: 201 Created
# {
#   "transfer_id": "unique_transfer_id",
#   "sender_transaction_id": 123,
#   "recipient_transaction_id": 124,
#   "amount": 25.00,
#   "sender_new_balance": 125.50,
#   "recipient_new_balance": 75.00,
#   "status": "completed"
# }

# Response: 400 Bad Request
# {
#   "error": "Insufficient balance",
#   "current_balance": 10.00,
#   "required_amount": 25.00
# }



@router.post('/')
async def create_transfer(transfer: TransferCreate, db: AsyncSession = Depends(get_db)):
    # Check if sender has enough balance
    sender = await crud.get_user(db=db, user_id=transfer.sender_user_id)
    if sender.balance < transfer.amount:
        raise HTTPException(status_code=400, detail={
            "error": "Insufficient balance",
            "current_balance": sender.balance,
            "required_amount": transfer.amount
        })

    # Create transactions for both sender and recipient
    sender_transaction = await crud.create_transaction(db=db, transaction=TransactionCreate(
        user_id=transfer.sender_user_id,
        transaction_type="debit",
        amount=transfer.amount,
        description=transfer.description,
        reference_transaction_id=None,
        recipient_user_id=transfer.recipient_user_id
    ))

    recipient_transaction = await crud.create_transaction(db=db, transaction=TransactionCreate(
        user_id=transfer.recipient_user_id,
        transaction_type="credit",
        amount=transfer.amount,
        description=transfer.description,
        reference_transaction_id=sender_transaction.id,
        recipient_user_id=transfer.sender_user_id
    ))

    # Update user balances
    await crud.update_user_balance(db=db, user_id=transfer.sender_user_id, amount=-transfer.amount)
    await crud.update_user_balance(db=db, user_id=transfer.recipient_user_id, amount=transfer.amount)

    return {
        "transfer_id": "unique_transfer_id",
        "sender_transaction_id": sender_transaction.id,
        "recipient_transaction_id": recipient_transaction.id,
        "amount": transfer.amount,
        "sender_new_balance": sender.balance - transfer.amount,
        "recipient_new_balance": recipient.balance + transfer.amount,
        "status": "completed"
    }