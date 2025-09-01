


from pydantic import BaseModel, Field
from datetime import datetime


# id = Column(Integer,primary_key=True, index=True)
# username=Column(String(50),nullable=False,unique=True)
# email= Column(String(100),nullable=False, unique=True)
# password=Column(String(255),nullable=False)
# phone_number=Column(String(15))
# balance=Column(DECIMAL(10,2),nullable=False,default=0.00)
# created_at=Column(TIMESTAMP,nullable=False,default=func.now())
# updated_at=Column(TIMESTAMP,nullable=False,default=func.now(),onupdate=func.now())
class UserBase(BaseModel):
    username: str =Field(..., max_length=50)
    email: str = Field(..., max_length=100)

class UserCreate(UserBase):
    pass 


class UserUpdate(UserBase):
    pass 

class UserResponse(UserBase):
    id : int 
    created_at: datetime
    updated_at: datetime



class Transaction(BaseModel):
    pass 