from fastapi import APIRouter, Depends
from internal.service.user import UserService
from internal import dependencies
from internal.models import user as model

router = APIRouter()

@router.get("/me")
async def get_me(service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    if not current_user:
        return {"status": "ok", "message": "please sign in"}
    return await service.get_me(current_user["gmail"])

@router.post('/signup')
async def sign_up(user: model.UserCreate, service: UserService = Depends(dependencies.get_user_service)):
    return await service.sign_up(user)

@router.get('/verify-gmail')
async def verify_gmail(token: str, service: UserService = Depends(dependencies.get_user_service)):
    return await service.verify_gmail(token)

@router.post('/signin')
async def sign_in(user: model.UserSignIn, service: UserService = Depends(dependencies.get_user_service)):
    return await service.singn_in(user)