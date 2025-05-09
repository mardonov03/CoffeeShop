from internal.repository.postgresql.user import UserRepository
from internal.core import security
from internal.models import user as model
from fastapi import HTTPException, Depends
import bcrypt
from internal.core.logging import logger
from internal.repository.redis.user import RedisUserRepository
from internal.tasks import mail
from internal.core import config
from internal import dependencies


class UserService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = UserRepository(pool)
        self.redis_repo = RedisUserRepository(redis_pool)

    async def get_user_count(self):
        return await self.psql_repo.get_user_count()

    async def get_me(self, gmail):
        return await self.psql_repo.get_user_data_from_gmail(gmail)

    async def sign_up(self, user: model.UserCreate):
        try:
            user_data = await self.psql_repo.get_user_data_from_gmail(user.gmail)
            if not user_data:

                count = await self.psql_repo.get_user_count()

                role = "superadmin" if count == 0 else "user"

                hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_password.decode('utf-8')

                await self.psql_repo.register_user(user, role)

                info = await self.send_verify_url(user.gmail)
                return info

            elif user_data['userid']:
                is_verified = await self.psql_repo.get_user_status(user_data['userid'])
                if not is_verified:
                    info = await self.send_verify_url(user.gmail)
                    return info
                else:
                    raise HTTPException(status_code=409, detail="Gmail already verified and registered.")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[sign_up error] {e}")
            raise HTTPException(status_code=500, detail='Registration error.')

    async def send_verify_url(self, gmail):
        try:
            token = await security.create_jwt_verify(gmail)
            verify_url = f"{config.settings.DNS_URL}/users/verify-gmail?token={token}"
            mail.send_verification_email.delay(gmail, verify_url)
            return {"status": "ok", "message": "verification link sent to email"}
        except Exception as e:
            logger.error(f'[send_verify_url error]: {e}')
            raise HTTPException(status_code=500, detail="error sending verification link")

    async def verify_gmail(self, token: str):
        try:
            payload = await security.decode_jwt_verify(token)
            if not payload:
                raise HTTPException(status_code=400, detail="Invalid or expired token")

            gmail = payload.get("sub")
            user = await self.psql_repo.get_user_data_from_gmail(gmail)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if user.account_status:
                return {"status": "ok", "message": "Email already verified"}

            await self.psql_repo.verify_user(model.VerifyGmail(gmail=gmail))

            return {"status": "ok", "message": "gmail successfully verified"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[verify_gmail error] {e}")
            raise HTTPException(status_code=500, detail="Internal error")

    async def singn_in(self, user: model.UserLogin):
        try:
            user_data = await self.psql_repo.get_user_data_from_gmail(user.gmail)
            if user_data and bcrypt.checkpw(user.password.encode('utf-8'), user_data['password'].encode('utf-8')):
                access_token = await security.create_jwt_token(user.gmail, 'access')
                refresh_token = await security.create_jwt_token(user.gmail, 'refresh')
                await self.psql_repo.add_refresh_token(refresh_token, user.userid)
                return {"status": "ok", "access_token": access_token}
        except Exception as e:
            logger.error(f'[singn_in error]: {e}')

    async def update_access_token(self, token: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[update_access_token error]: {e}')