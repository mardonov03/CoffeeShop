from internal.repository.postgresql.user import UserRepository

class UserRepo:
    def __init__(self, pool):
        self.user = UserRepository(pool)