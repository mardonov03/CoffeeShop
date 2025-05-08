import aioredis
from internal.core import config
from internal.core.logging import logger

async def create_redis():
    try:
        redis = await aioredis.from_url(f"redis://{config.settings.REDIS_HOST}:{config.settings.REDIS_PORT}",decode_responses=True)
        return redis
    except Exception as e:
        logger.error(f"create_redis error: {e}")
