class RedisUserRepository:
    def __init__(self, redis):
        self.redis = redis