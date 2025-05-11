from internal.core.logging import logger
from internal.models import user as model
from typing import Optional
from internal.tasks import user as tasks
import datetime

class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def register_user(self, user: model.UserCreate, role: str):
        try:
            async with self.pool.acquire() as conn:
                userid = await conn.fetchval('INSERT INTO users (gmail, password, role, full_name) VALUES ($1, $2, $3, $4) RETURNING userid',user.gmail, user.password, role, user.full_name)
                await conn.execute('INSERT INTO user_status (userid) VALUES ($1)',userid)
                await conn.execute('INSERT INTO cart (userid) VALUES ($1)',userid)
                await conn.execute('INSERT INTO user_tokens (userid) VALUES ($1)',userid)
                tasks.delete_user.apply_async(countdown=300, args=[user.gmail])

        except Exception as e:
            logger.error(f'[register_user error]: {e}')

    async def verify_user(self, user: model.VerifyGmail):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("UPDATE user_status SET is_verified = TRUE FROM users WHERE user_status.userid = users.userid AND users.gmail = $1", user.gmail)
        except Exception as e:
            logger.error(f'[verify_user error]: {e}')

    async def get_user_count(self) -> Optional[int]:
        try:
            async with self.pool.acquire() as conn:
                count = await conn.fetchval('SELECT COUNT(*) FROM users')
                return count
        except Exception as e:
            logger.error(f'get_user_count error: {e}')
            return None

    async def get_user_data_from_gmail(self, gmail: str):
        try:
            async with self.pool.acquire() as conn:
                user_data = await conn.fetchrow("SELECT u.*, us.is_verified as account_status FROM users u LEFT JOIN user_status us ON u.userid = us.userid WHERE u.gmail = $1", gmail)
                if user_data:
                    return model.UserInfo(**dict(user_data))
                return None
        except Exception as e:
            logger.error(f"[get_user_data_from_gmail error]: {e}")
            return {"status": 'error'}

    async def get_user_data_from_id(self, userid: int):
        try:
            async with self.pool.acquire() as conn:
                user_data = await conn.fetchrow("SELECT u.*, us.is_verified as account_status FROM users u LEFT JOIN user_status us ON u.userid = us.userid WHERE u.userid = $1", userid)
                if user_data:
                    return model.UserInfo(**dict(user_data))
                return None
        except Exception as e:
            logger.error(f"[get_user_data_from_id error]: {e}")
            return {"status": 'error'}

    async def patch_users(self, for_user: int, data: model.UserUpdate):
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow("UPDATE users SET full_name = $1, gmail = $2, role = $3 WHERE userid = $4 RETURNING *", data.full_name, data.gmail, data.role, for_user)
            return result
        except Exception as e:
            logger.error(f'[patch_users error]: {e}')

    async def delete_user_from_id(self, userid: int):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM users WHERE userid=$1", userid)
                return {"status": "ok"}
        except Exception as e:
            logger.error(f'[delete_user_from_id error]: {e}')
            return {"status": "error"}

    async def get_users(self):
        try:
            async with self.pool.acquire() as conn:
                users = await conn.fetch("SELECT u.*, us.is_verified as account_status FROM users u LEFT JOIN user_status us ON u.userid = us.userid")
                users_list = [model.UserInfo(**user) for user in users]
                return {"status": 'ok', "users": users_list}
        except Exception as e:
            logger.error(f'[get_users error]: {e}')

    async def get_user_status(self, userid) -> bool:
        try:
            async with self.pool.acquire() as conn:
                data = await conn.fetchrow("SELECT is_verified FROM user_status WHERE userid = $1", userid)
                if data:
                    return data["is_verified"]
                return False
        except Exception as e:
            logger.error(f'[get_user_status error]: {e}')
            return False

    async def is_verified(self, gmail) -> bool:
        try:
            async with self.pool.acquire() as conn:
                is_verified = await conn.fetchval("SELECT is_verified FROM user_status JOIN users ON users.userid = user_status.userid WHERE users.gmail = $1", gmail)
                return is_verified if is_verified is not None else False
        except Exception as e:
            logger.warning(f'[is_verified warning]: {e}')

    async def get_refresh_token(self, gmail: str):
        try:
            async with self.pool.acquire() as conn:
                query = """
                    SELECT ut.refresh_token
                    FROM user_tokens ut
                    JOIN users u ON u.userid = ut.userid
                    WHERE u.gmail = $1
                """
                refresh_token = await conn.fetchval(query, gmail)
                return {"status": "ok", "token": refresh_token}
        except Exception as e:
            logger.error(f'[get_refresh_token error]: {e}')
            return {"status": "error", "token": None}

    async def delete_user(self, gmail: str):
        try:
            async with self.pool.acquire() as conn:
                user = await conn.fetchrow("SELECT userid FROM users WHERE gmail=$1", gmail)
                if not user:
                    logger.warning("User not found")
                    return

                userid = user["userid"]

                await conn.execute("DELETE FROM users WHERE userid=$1", userid)
        except Exception as e:
            logger.error(f'[delete_user error]: {e}')

    async def add_refresh_token(self, token: str, gmail: str):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('UPDATE user_tokens ut SET refresh_token = $1, expires_at = $2 FROM users u WHERE u.gmail = $3 AND ut.userid = u.userid',token, datetime.datetime.now(), gmail)
        except Exception as e:
            logger.error(f'[add_refresh_token error]: {e}')