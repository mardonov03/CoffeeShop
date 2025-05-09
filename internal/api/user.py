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

@router.get("/me")
async def get_me(service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    if not current_user:
        return {"status": "ok", "message": "please sign in"}
    return await service.get_me(current_user["sub"])

@router.get("/")
async def get_users(service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    if not current_user:
        return {"status": "ok", "message": "please sign in"}
    return await service.get_users(current_user["sub"])

@router.get("/{id}")
async def get_user_data_from_id(id:int, service: UserService = Depends(dependencies.get_user_service)):
    return await service.get_user_data_from_id(id)

@router.patch("/{id}")
async def patch_users(id: int, user: model.UserUpdate, service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    if not current_user:
        return {"status": "ok", "message": "please sign in"}
    return await service.patch_users(id, user, current_user["sub"])

@router.delete("/{id}")
async def delete_users(id: int, service: UserService = Depends(dependencies.get_user_service), current_user: dict = Depends(dependencies.get_current_user)):
    if not current_user:
        return {"status": "ok", "message": "please sign in"}
    return await service.delete_users(id, current_user["sub"])

