from internal.service.user import UserService
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from internal.core import security
from fastapi import Depends, Request
from internal.core.logging import logger
import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_user_service(request: Request) -> UserService:
    return UserService(request.app.state.pool, request.app.state.redis_pool)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    try:
        if token is None:
            return None
        payload = await security.decode_jwt_token(token)
        return payload
    except Exception as e:
        logger.error(f'[get_current_user error]: {e}')