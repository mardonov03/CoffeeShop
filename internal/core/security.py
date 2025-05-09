from jose import jwt, JWTError
from internal.core import config
from datetime import datetime, timedelta
from internal.core.logging import logger
from typing import Optional

async def create_jwt_token(username: str) -> Optional[str]:
    try:
        expiration = datetime.utcnow() + timedelta(minutes=config.settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": username.lower(), "exp": expiration}
        return jwt.encode(payload, config.settings.SECRET_KEY, algorithm=config.settings.ALGORITHM)
    except Exception as e:
        logger.error(f'[create_jwt_token] {e}')
        return None


async def decode_jwt_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        if 'sub' not in payload or 'exp' not in payload:
            return None
        return payload
    except JWTError as e:
        logger.warning(f'"decode_jwt_token error": {e}')
        return None

async def create_jwt_verify(username: str) -> Optional[str]:
    try:
        expiration = datetime.utcnow() + timedelta(minutes=5)
        payload = {"sub": username.lower(), "exp": expiration}
        return jwt.encode(payload, config.settings.SECRET_KEY_VERIFY, algorithm=config.settings.ALGORITHM)
    except Exception as e:
        logger.error(f'[create_jwt_token] {e}')
        return None

async def decode_jwt_verify(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY_VERIFY, algorithms=[config.settings.ALGORITHM])
        if 'sub' not in payload or 'exp' not in payload:
            return None
        return payload
    except JWTError as e:
        logger.warning(f'"decode_jwt_token error": {e}')
        return None