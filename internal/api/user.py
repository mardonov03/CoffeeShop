from fastapi import APIRouter, Depends
from internal.service.user import UserService
from internal import dependencies
from internal.core.logging import logger
from internal.models import user as model

router = APIRouter()

@router.get("/count") # бу хозрча турсн кейнчали регистрация пайтида бринчи .зер админ клшчун кере
async def get_user_count(service: UserService = Depends(dependencies.get_user_service)):
    return await service.get_user_count()

@router.get("/me")
async def get_me(service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    return await service.get_me(current_user["username"])

@router.post('/signup')
async def sign_up(user: model.UserCreate, service: UserService = Depends(dependencies.get_user_service)):
    return await service.sign_up(user)

@router.post('/verify-email')
async def verify_email(code: model.VerifyGmail, service: UserService = Depends(dependencies.get_user_service)):
    return await service.verify_email(code)

@router.post('/signin')
async def sign_in(user: model.UserLogin, service: UserService = Depends(dependencies.get_user_service)):
    pass
