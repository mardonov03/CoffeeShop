from jose import jwt, JWTError
from internal.core import config
async def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        return payload
    except JWTError:
        return {}
