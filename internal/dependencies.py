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

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)):
    try:
        if token is None:
            return None

        payload = await security.decode_jwt_token(token)

        if payload.get("exp") and datetime.datetime.fromtimestamp(payload["exp"]) < datetime.datetime.utcnow():
            refresh_token = payload.get("refresh_token")
            if not refresh_token:
                return None

            response = await service.refresh_access_token(refresh_token)
            if response["status"] == "ok":
                payload["access_token"] = response["access_token"]
                payload["refresh_token"] = response["refresh_token"]
                payload["exp"] = response["exp"]
        return payload
    except Exception as e:
        logger.error(f'[get_current_user error]: {e}')
        return None
