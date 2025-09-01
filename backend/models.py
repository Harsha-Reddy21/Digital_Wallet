from database import Base 
from sqlalchemy import Column, String, Text, Table, ForeignKey, Float, Integer,DECIMAL,TIMESTAMP
from sqlalchemy.sql import func
import enum

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True, index=True)
    username=Column(String(50),nullable=False,unique=True)
    email= Column(String(100),nullable=False, unique=True)
    password=Column(String(255),nullable=False)
    phone_number=Column(String(15))
    balance=Column(DECIMAL(10,2),nullable=False,default=0.00)
    created_at=Column(TIMESTAMP,nullable=False,default=func.now())
    updated_at=Column(TIMESTAMP,nullable=False,default=func.now(),onupdate=func.now())



class TransactionType(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"


class Transaction(Base):
    __tablename__='transactions'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    transaction_type=Column(String(20),nullable=False)
    amount=Column(DECIMAL(10,2),nullable=False)
    description=Column(Text)
    reference_transaction_id=Column(Integer,ForeignKey('transactions.id'))
    recipient_user_id=Column(Integer,ForeignKey('users.id'))
    created_at=Column(TIMESTAMP,nullable=False,default=func.now())
