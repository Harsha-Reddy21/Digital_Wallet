
from fastapi import APIRouter
import crud
router=APIRouter(prefix='/users')


# GET /users/{user_id}
# Response: 200 OK
# {
#   "user_id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "phone_number": "+1234567890",
#   "balance": 150.50,
#   "created_at": "2024-01-01T00:00:00Z"
# }

@router.get('/{user_id}',response_model=crud.schemas.UserResponse)
async def get_user(user_id:int):
    user = await crud.get_user(user_id=user_id)
    if user is None:
        return {"error": "User not found"}
    return user

