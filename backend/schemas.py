

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
    reference_transaction_id: int
    recipient_user_id: int
    transaction_type: str
    created_at: datetime
    updated_at: datetime
    id: int
    created_at: datetime
    updated_at: datetime


