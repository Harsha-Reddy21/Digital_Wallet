


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str =Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    phone_number: Optional[str] = Field(None, max_length=15)    
    balance: Optional[float] = 0.00

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6, max_length=255)

class UserResponse(UserBase):
    user_id:int
    created_at: datetime
    updated_at: datetime




class Transaction(BaseModel):
    pass 