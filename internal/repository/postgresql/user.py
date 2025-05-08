from internal.core.logging import logger
from internal.models import user as model
from typing import Optional
class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def register_user(self, user: model.UserCreate, role: str):
        try:
            async with self.pool.acquire() as conn:
                userid = await conn.fetchval('INSERT INTO users (gmail, username, password, role) VALUES ($1, $2, $3, $4) RETURNING userid',user.gmail, user.username, user.password, role)
                await conn.execute('INSERT INTO user_status (userid) VALUES ($1)',userid)
                await conn.execute('INSERT INTO basket (userid) VALUES ($1)',userid)

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