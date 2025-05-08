from internal.core.logging import logger
from internal.models import user

class UserRepository:
    def __init__(self, pool):
        self.pool = pool
    async def register_user(self):
        try:
            pass
        except Exception as e:
            logger.error(f'"RegisterUser error": {e}')


    async def get_user_count(self):
        try:
            return {'count': 12}
        except Exception as e:
            logger.error(f'"GetUserCount error": {e}')

    async def get_user_data(self, username):
        try:
            async with self.pool.acquire() as conn:
                data = await conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
                if data:
                    return user.UserCreate(**dict(data))
                return None
        except Exception as e:
            logger.error(f'"GetUserData error": {e}')