from internal.repository.postgresql.user import UserRepository
from internal.core.security import create_jwt_token
from internal.models import user as model
from fastapi import HTTPException
import bcrypt
from datetime import datetime
from internal.core.logging import logger
from internal.repository.redis.user import RedisUserRepository
from internal.tasks import mail

class UserService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = UserRepository(pool)
        self.redis_repo = RedisUserRepository(redis_pool)

    async def get_user_count(self):
        return await self.psql_repo.get_user_count()

    async def get_me(self, username):
        return await self.psql_repo.get_user_data(username)

    async def sign_up(self, user: model.UserCreate, tokenuser: dict):
        try:
            user_data = await self.psql_repo.get_user_data(user.gmail)
            if not user_data:
                await self.send_code(user.gmail)
                return {"status": "ok", "message": "verification code sent to email"}

            if user_data['gmail'] and user_data['account_status']:
                raise HTTPException(status_code=409, detail='Gmail already registered.')

            if user_data['username']:
                raise HTTPException(status_code=408, detail='Username already taken.')

            if user_data.get('statuscode') and not tokenuser:
                raise HTTPException(status_code=400, detail="Finish setup on verified device.")

            # Продолжение регистрации
            hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
            count = await self.psql_repo.get_active_user_count()
            role = self._get_role(user.gmail, count)
            await self.psql_repo.finalize_registration(user.username, hashed_pw, user.gmail, role)
            logger.info(f"User created: {user.username}, role: {role}")
            token = await create_jwt_token(user.username)
            return {'token_access': token, 'gmail': user.gmail}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[sign_up error] {e}")
            raise HTTPException(status_code=500, detail='Registration error.')

    def _get_role(self, gmail: str, user_count: int) -> str:
        if gmail in self.psql_repo.admin_emails:
            return 'admin'
        return 'superadmin' if user_count == 0 else 'user'

    async def send_code(self, gmail):
        try:
            is_code_sended = await self.redis_repo.get_verify_code(gmail)
            if is_code_sended:
                return {"status": "ok", "message": "сode already sent"}
            redis_code = await self.redis_repo.gen_code(gmail)
            mail.send_verification_email.delay(gmail, redis_code)
        except Exception as e:
            logger.error(f'"send_code error": {e}')
            raise HTTPException(status_code=500, detail="error sending verification code")