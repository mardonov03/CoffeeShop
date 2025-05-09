from internal.repository.redis.menu import RedisMenuRepository
from internal.repository.postgresql.menu import MenuRepository


class MenuService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = MenuRepository(pool)
        self.redis_repo = RedisMenuRepository(redis_pool)
