from internal.repository.postgresql.user import UserRepository
from internal.core.security import create_jwt_token
from internal.models import user as model
from fastapi import HTTPException
import bcrypt
from datetime import datetime
from internal.core.logging import logger
import uuid

class UserService:
    def __init__(self, pool):
        self.repo = UserRepository(pool)

    async def get_user_count(self):
        return await self.repo.get_user_count()

    async def get_me(self, username):
        return await self.repo.get_user_data(username)

    async def sign_up(self, user: model.UserCreate, tokenuser: dict):
        try:
            user_data = await self.repo.get_user_data(user.gmail)
            if not user_data:
                pass
            user_gmail = user_data['user_gmail']
            logger.info(f"Checking registration conditions for {user.gmail}")

            if user_gmail and user_gmail['account_status']:
                raise HTTPException(status_code=409, detail='Gmail already registered.')

            if user_data['username']:
                raise HTTPException(status_code=408, detail='Username already taken.')

            if user_gmail and not user_gmail['account_status'] and not user_gmail['statuscode']:
                last_sent = user_gmail['time_for_verificy_code']
                if (datetime.now() - last_sent).total_seconds() < 60:
                    raise HTTPException(status_code=429, detail='Retry after 60s.')

            if user_gmail and user_gmail['statuscode'] and tokenuser is None:
                raise HTTPException(status_code=400, detail='Finish setup on verified device.')

            if tokenuser and tokenuser.get('sub') == user.gmail:
                hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
                count = await self.repo.get_active_user_count()
                role = self._get_role(user.gmail, count)
                await self.repo.finalize_registration(user.username, hashed_pw, user.gmail, role)
                logger.info(f"User created: {user.username}, role: {role}")
                token = await create_jwt_token(user.username)
                return {'token_access': token, 'gmail': user.gmail}

            await self.repo.send_verification_email(user.gmail)
            logger.info(f"Verification code sent to {user.gmail}")
            return f'Код подтверждения отправлен на: {user.gmail}'

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[sign_up error] {e}")
            raise HTTPException(status_code=500, detail='Registration error.')

    def _get_role(self, gmail: str, user_count: int) -> str:
        if gmail in self.repo.admin_emails:
            return 'admin'
        return 'superadmin' if user_count == 0 else 'user'

    async def send_code(gmail):
        try:
            pass
        except Exception as e:
            logger.error(f'"send_code error": {e}')