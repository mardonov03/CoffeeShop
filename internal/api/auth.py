from fastapi import APIRouter, Depends
from internal.service.user import UserService
from internal import dependencies
from internal.models import user as model

router = APIRouter()

@router.post('/signup')
async def sign_up(user: model.UserCreate, service: UserService = Depends(dependencies.get_user_service)):
    return await service.sign_up(user)

@router.post('/refresh')
async def refresh_access_token(refresh_token: str, service: UserService = Depends(dependencies.get_user_service)):
    return await service.refresh_access_token(refresh_token)

@router.get('/verify-gmail')
async def verify_gmail(token: str, service: UserService = Depends(dependencies.get_user_service)):
    return await service.verify_gmail(token)

@router.post('/signin')
async def sign_in(user: model.UserSignIn, service: UserService = Depends(dependencies.get_user_service)):
    return await service.singn_in(user)
