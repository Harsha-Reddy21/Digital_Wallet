
from database import Base, get_db, AsyncSession
from fastapi import Depends
from sqlalchemy import select

import models
import schemas


async def get_user(db:AsyncSession=Depends(get_db), user_id:int=None):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    return user

