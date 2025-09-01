
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from database import AsyncSession, get_db
import crud
import schemas
router = APIRouter(prefix='/transfer', tags=['Transfer'])


@router.post('/')
async def transfer_money(transfer: schemas.TransferCreate, db: AsyncSession = Depends(get_db)):
    sender = await crud.get_user(db=db, user_id=transfer.sender_user_id)
    recipient = await crud.get_user(db=db, user_id=transfer.recipient_user_id)

    if sender is None or recipient is None:
        raise HTTPException(status_code=404, detail="User not found")

    if sender.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Update balances
    sender.balance -= transfer.amount
    recipient.balance += transfer.amount
    await db.commit()
    await db.refresh(sender)
    await db.refresh(recipient)

    # Create sender transaction (TRANSFER_OUT)
    sender_transaction_data = schemas.TransferTransactionCreate(
        user_id=transfer.sender_user_id,
        amount=transfer.amount,
        description=transfer.description,
        transaction_type="TRANSFER_OUT",
        recipient_user_id=transfer.recipient_user_id
    )
    sender_transaction = await crud.create_transfer_transaction(db=db, transaction=sender_transaction_data)

    # Create recipient transaction (TRANSFER_IN) with reference to sender transaction
    recipient_transaction_data = schemas.TransferTransactionCreate(
        user_id=transfer.recipient_user_id,
        amount=transfer.amount,
        description=transfer.description,
        transaction_type="TRANSFER_IN",
        recipient_user_id=transfer.recipient_user_id,
        reference_transaction_id=sender_transaction.id
    )
    recipient_transaction = await crud.create_transfer_transaction(db=db, transaction=recipient_transaction_data)

    # Update sender transaction with reference to recipient transaction
    sender_transaction.reference_transaction_id = recipient_transaction.id
    await db.commit()
    await db.refresh(sender_transaction)

    return {
        "transfer_id": f"transfer_{sender_transaction.id}_{recipient_transaction.id}",
        "sender_transaction_id": sender_transaction.id,
        "recipient_transaction_id": recipient_transaction.id,
        "amount": transfer.amount,
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance,
        "status": "completed"
    }




@router.get('/{transfer_id}')
async def get_transfer(transfer_id: str, db: AsyncSession = Depends(get_db)):
    transfer = await crud.get_transfer(db=db, transfer_id=transfer_id)
    if transfer is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer
