from fastapi import APIRouter, Depends
from internal.service.user import UserService
from internal import dependencies
from internal.core.logging import logger
from internal.models import user as models

router = APIRouter()

@router.get("/me")
async def get_me(service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    return await service.get_me(current_user["username"])

@router.post('/signup')
async def sign_up(user: models.UserCreate, service: UserService = Depends(dependencies.get_user_service)):
    return await service.sign_up(user)

@router.post('/signin')
async def sign_in(user: models.UserLogin, service: UserService = Depends(dependencies.get_user_service)):
    pass
