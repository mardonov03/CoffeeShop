from internal.core.logging import logger
import uuid
import bcrypt

class RedisUserRepository:
    def __init__(self, redis):
        self.redis = redis

    async def gen_code(self, gmail: str, expire: int = 300):
        try:
            code = str(uuid.uuid4())[:8]
            hashcode = bcrypt.hashpw(code.encode('utf-8'), bcrypt.gensalt(rounds=12))

            await self.redis.set(f"verify:{gmail}", hashcode, ex=expire)

            return code
        except Exception as e:
            logger.error(f'"redis gen_code error": {e}')
            return None

    async def get_verify_code(self, gmail: str):
        try:
            return await self.redis.get(f"verify:{gmail}")
        except Exception as e:
            logger.error(f'"redis get_verify_code error": {e}')
