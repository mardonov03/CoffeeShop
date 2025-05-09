class RedisUserRepository:
    def __init__(self, redis):
        self.redis = redis

    async def set_verify_block(self, gmail: str, ttl: int = 300):
        await self.redis.set(f"verify_block:{gmail}", "1", ex=ttl)

    async def is_verify_blocked(self, gmail: str) -> bool:
        return await self.redis.exists(f"verify_block:{gmail}") == 1