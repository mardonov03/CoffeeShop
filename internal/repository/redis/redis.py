from internal.repository.redis.user import RedisUserRepository

class RedisRepo:
    def __init__(self, redis):
        self.user = RedisUserRepository(redis)
