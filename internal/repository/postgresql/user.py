from internal.core.logging import logger
from internal.models import user as model
from typing import Optional
from internal.tasks import user as tasks

class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def register_user(self, user: model.UserCreate, role: str):
        try:
            async with self.pool.acquire() as conn:
                userid = await conn.fetchval('INSERT INTO users (gmail, username, password, role, full_name) VALUES ($1, $2, $3, $4, $5) RETURNING userid',user.gmail, user.username, user.password, role, user.full_name)
                await conn.execute('INSERT INTO user_status (userid) VALUES ($1)',userid)
                await conn.execute('INSERT INTO basket (userid) VALUES ($1)',userid)
                tasks.delete_user.apply_async(countdown=300, args=[user.gmail])

        except Exception as e:
            logger.error(f'"register_user error": {e}')

    async def verify_user(self, user: model.VerifyGmail):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("UPDATE user_status SET is_verified = TRUE FROM users WHERE user_status.userid = users.userid AND users.gmail = $1", user.gmail)
        except Exception as e:
            logger.error(f'"verify_user error": {e}')


    async def get_user_count(self) -> Optional[int]:
        try:
            async with self.pool.acquire() as conn:
                count = await conn.fetchval('SELECT COUNT(*) FROM users')
                return count
        except Exception as e:
            logger.error(f'get_user_count error: {e}')
            return None

    async def get_user_data(self, username):
        try:
            async with self.pool.acquire() as conn:
                data = await conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
                if data:
                    return model.UserInfo(**dict(data))
                return None
        except Exception as e:
            logger.error(f'"get_user_data error": {e}')

    async def get_user_data_from_gmail(self, gmail: str):
        try:
            async with self.pool.acquire() as conn:
                user_data = await conn.fetchrow("SELECT u.*, us.is_verified as account_status FROM users u LEFT JOIN user_status us ON u.userid = us.userid WHERE u.gmail = $1", gmail)
                if user_data:
                    return model.UserInfo(**dict(user_data))

                return None
        except Exception as e:
            logger.error(f"get_user_data_from_gmail error: {e}")
            return None

    async def get_user_status(self, userid) -> bool:
        try:
            async with self.pool.acquire() as conn:
                data = await conn.fetchrow("SELECT is_verified FROM user_status WHERE userid = $1", userid)
                if data:
                    return data["is_verified"]
                return False
        except Exception as e:
            logger.error(f'"get_user_status error": {e}')
            return False

    async def is_verified(self, gmail) -> bool:
        try:
            async with self.pool.acquire() as conn:
                is_verified = await conn.fetchval("SELECT is_verified FROM user_status JOIN users ON users.userid = user_status.userid WHERE users.gmail = $1", gmail)
                return is_verified if is_verified is not None else False
        except Exception as e:
            logger.warning(f'[is_verified warning]: {e}')
            return False

    async def delete_user_by_gmail(self, gmail: str):
        try:
            logger.info("try to delete delete_user_by_gmail")
            logger.info(gmail)
            async with self.pool.acquire() as conn:
                await conn.execute('DELETE FROM users WHERE gmail=$1',gmail)
        except Exception as e:
            logger.error(f'[delete_user_by_gmail error]: {e}')