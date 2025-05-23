from internal.repository.postgresql.user import UserRepository
from internal.core import security
from internal.models import user as model
from fastapi import HTTPException, Depends
import bcrypt
from internal.core.logging import logger
from internal.repository.redis.user import RedisUserRepository
from internal.tasks import mail
from internal.core import config
from datetime import datetime, timedelta

class UserService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = UserRepository(pool)
        self.redis_repo = RedisUserRepository(redis_pool)

    async def get_user_count(self):
        return await self.psql_repo.get_user_count()

    async def get_me(self, gmail):
        try:
            data = await self.psql_repo.get_user_data_from_gmail(gmail)
            if data:
                return {"status": 'ok', "user_data": data}
        except Exception as e:
            logger.error(f'[get_me error]: {e}')
            return {"status": 'error'}

    async def patch_users(self, for_user: int, user: model.UserUpdate, gmail: str):
        try:
            data = await self.psql_repo.get_user_data_from_gmail(gmail)

            if data:

                if data.role not in ['admin', 'superadmin']:
                    raise HTTPException(status_code=403, detail="You do not have permission to update users")

                for_user_data = await self.psql_repo.get_user_data_from_id(for_user)

                if user.full_name is not None:
                    for_user_data.full_name = user.full_name
                if user.gmail is not None:
                    for_user_data.gmail = user.gmail
                if user.role is not None:
                    for_user_data.role = user.role

                updated_user = await self.psql_repo.patch_users(for_user, for_user_data)

                return {"status": "ok", "message": "User updated successfully", "user": updated_user}
        except Exception as e:
            logger.error(f'[patch_users error]: {e}')

    async def delete_users(self, userid: int, gmail: str):
        try:
            is_admin = await self.is_admin(gmail)
            if is_admin:
                await self.psql_repo.delete_user_from_id(userid)
                return {"status": "ok"}
        except Exception as e:
            logger.error(f'[delete_users error]: {e}')
            raise HTTPException(status_code=500, detail='Delete users error.')
    async def is_admin(self, gmail:str) -> bool:
        try:
            data = await self.psql_repo.get_user_data_from_gmail(gmail)
            if data and data.role in ['admin', 'superadmin']:
                return True
            return False
        except Exception as e:
            logger.error(f'[is_admin error]: {e}')
            return False

    async def get_users(self, gmail):
        try:
            is_admin = await self.is_admin(gmail)
            if is_admin:
                users = await self.psql_repo.get_users()
                if users['status']=="ok":
                    return users
        except Exception as e:
            logger.error(f'[get_me error]: {e}')
            return {"status": 'error'}

    async def get_user_data_from_id(self, userid):
        try:
            data = await self.psql_repo.get_user_data_from_id(userid)
            if data:
                return {"status": 'ok', "user_data": data}
        except Exception as e:
            logger.error(f'[get_user_data_from_id error]: {e}')
            return {"status": 'error'}

    async def sign_up(self, user: model.UserCreate):
        try:
            user_data = await self.psql_repo.get_user_data_from_gmail(user.gmail)

            if await self.redis_repo.is_verify_blocked(user.gmail):
                raise HTTPException(status_code=429, detail="Verification already sent. Try again later.")

            if not user_data:

                count = await self.psql_repo.get_user_count()

                role = "superadmin" if count == 0 else "user"

                hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_password.decode('utf-8')

                await self.psql_repo.register_user(user, role)

                info = await self.send_verify_url(user.gmail)
                await self.redis_repo.set_verify_block(user.gmail)
                return info

            elif user_data.userid:
                is_verified = await self.psql_repo.get_user_status(user_data.userid)
                if not is_verified:
                    info = await self.send_verify_url(user.gmail)
                    await self.redis_repo.set_verify_block(user.gmail)
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
            verify_url = f"{config.settings.DNS_URL}/auth/verify-gmail?token={token}"
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
                return {"status": "no", "message": "Email already verified"}

            await self.psql_repo.verify_user(model.VerifyGmail(gmail=gmail))

            return {"status": "ok", "message": "gmail successfully verified"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[verify_gmail error] {e}")
            raise HTTPException(status_code=500, detail="Internal error")

    async def singn_in(self, user: model.UserSignIn):
        try:
            user_data = await self.psql_repo.get_user_data_from_gmail(user.gmail)
            if user_data and bcrypt.checkpw(user.password.encode('utf-8'), user_data.password.encode('utf-8')):
                access_token = await security.create_jwt_token(user.gmail, 'access')
                refresh_token = await security.create_jwt_token(user.gmail, 'refresh')
                await self.psql_repo.add_refresh_token(refresh_token, user.gmail)
                return {"status": "ok", "access_token": access_token}
            else:
                return {"status": 'ok', "message": 'there is no such account'}
        except Exception as e:
            logger.error(f'[singn_in error]: {e}')
            return {"status": "error", "message": 'server error, please try again'}

    async def refresh_access_token(self, refresh_token: str):
        try:
            payload = await security.decode_jwt_token(refresh_token)
            if not payload:
                raise HTTPException(status_code=400, detail="Invalid or expired token")

            gmail = payload.get("sub")
            db_token = await self.psql_repo.get_refresh_token(gmail)

            if db_token['token'] != refresh_token:
                raise HTTPException(status_code=404, detail="Server error please sign in again")

            access_token = await security.create_jwt_token(gmail, 'access')
            refresh_token = await security.create_jwt_token(gmail, 'refresh')
            exp = datetime.utcnow() + timedelta(minutes=config.settings.JWT_ACCESS_EXPIRE_MINUTES)

            await self.psql_repo.add_refresh_token(refresh_token, gmail)

            return {"status": 'ok', "access_token": access_token, "refresh_token": refresh_token, "exp": exp}
        except Exception as e:
            logger.error(f'[refresh_access_token error]: {e}')
            raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")

    async def is_cart_belongs(self, gmail: str, cartid: int):
        return await self.psql_repo.is_cart_belongs(gmail, cartid)