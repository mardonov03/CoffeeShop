from internal.core.logging import logger
import json

class RedisUserRepository:
    def __init__(self, redis):
        self.redis = redis

    async def set_verify_code(self, gmail: str, code: str, expire: int = 300):
        try:
            await self.redis.set(f"verify:{gmail}", code, ex=expire)
        except Exception as e:
            logger.error(f'"redis set_verify_code error": {e}')

    async def get_verify_code(self, gmail: str):
        try:
            return await self.redis.get(f"verify:{gmail}")
        except Exception as e:
            logger.error(f'"redis get_verify_code error": {e}')
