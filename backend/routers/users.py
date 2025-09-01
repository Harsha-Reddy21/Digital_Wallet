
from fastapi import APIRouter,Depends
import crud
import schemas 
from database import get_db,async_sessionmaker,AsyncSession
router=APIRouter(prefix='/users')




@router.get('/{user_id}')
async def get_user(user_id:int, db:AsyncSession=Depends(get_db)):
    user = await crud.get_user(db=db, user_id=user_id)
    if user is None:
        return {"error": "User not found"}
    return user


@router.post('/',response_model=schemas.UserResponse)
async def create_user(db:AsyncSession=Depends(get_db), user:schemas.UserCreate=None):
    return await crud.create_user(db=db, user=user)


@router.put('/{user_id}')
async def update_user(user_id:int, db:AsyncSession=Depends(get_db), user:schemas.UserUpdate=None):
    return await crud.update_user(db=db, user_id=user_id, user=user)
