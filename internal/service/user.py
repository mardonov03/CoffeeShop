from internal.repository.postgresql.user import UserRepository
from internal.core.security import create_jwt_token
from internal.models import user as model
from fastapi import HTTPException
import bcrypt
from datetime import datetime
from internal.core.logging import logger
import uuid
from internal.repository.redis.user import RedisUserRepository

class UserService:
    def __init__(self, pool, redis_pool):
        self.repo = UserRepository(pool)
        self.redis = RedisUserRepository(redis_pool)

    async def get_user_count(self):
        return await self.repo.get_user_count()

    async def get_me(self, username):
        return await self.repo.get_user_data(username)

    async def sign_up(self, user: model.UserCreate, tokenuser: dict):
        try:
            user_data = await self.repo.get_user_data(user.gmail)
            if not user_data:
                return {"message": "User not found."}

            # Уточнение условий
            if user_data['gmail'] and user_data['account_status']:
                raise HTTPException(status_code=409, detail='Gmail already registered.')

            if user_data['username']:
                raise HTTPException(status_code=408, detail='Username already taken.')

            if user_data.get('statuscode') and not tokenuser:
                raise HTTPException(status_code=400, detail="Finish setup on verified device.")

            # Продолжение регистрации
            hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
            count = await self.repo.get_active_user_count()
            role = self._get_role(user.gmail, count)
            await self.repo.finalize_registration(user.username, hashed_pw, user.gmail, role)
            logger.info(f"User created: {user.username}, role: {role}")
            token = await create_jwt_token(user.username)
            return {'token_access': token, 'gmail': user.gmail}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[sign_up error] {e}")
            raise HTTPException(status_code=500, detail='Registration error.')

    def _get_role(self, gmail: str, user_count: int) -> str:
        if gmail in self.repo.admin_emails:
            return 'admin'
        return 'superadmin' if user_count == 0 else 'user'

    async def send_code(self, gmail):
        try:
            redis_code = await self.repo.redis.user.get_verify_code(gmail)
            if redis_code:
                await self.repo.send_verification_email(gmail, redis_code)
                return {"status": "success", "message": "Verification code sent successfully."}
            else:
                raise HTTPException(status_code=404, detail="Verification code not found.")
        except Exception as e:
            logger.error(f'"send_code error": {e}')
            raise HTTPException(status_code=500, detail="Error sending verification code.")
