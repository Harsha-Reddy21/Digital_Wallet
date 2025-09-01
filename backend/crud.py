
from database import Base, get_db, AsyncSession
from fastapi import Depends
from sqlalchemy import select

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

async def update_user(db:AsyncSession, user_id:int, user:schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user is None:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user




