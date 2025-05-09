from internal.repository.postgresql.user import UserRepository
from internal.repository.postgresql.menu import MenuRepository

class UserRepo:
    def __init__(self, pool):
        self.user = UserRepository(pool)
        self.menu = MenuRepository(pool)