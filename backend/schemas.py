

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    phone_number: str
    balance: float  

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime



class TransactionBase(BaseModel):
    user_id: int
    amount: float
    description: str
    


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    transaction_type: str
    reference_transaction_id: Optional[int] = None
    recipient_user_id: Optional[int] = None
    created_at: datetime


class TransferCreate(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str

class TransferTransactionCreate(BaseModel):
    user_id: int
    amount: float
    description: str
    transaction_type: str
    recipient_user_id: Optional[int] = None
    reference_transaction_id: Optional[int] = None

