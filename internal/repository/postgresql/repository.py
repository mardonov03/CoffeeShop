from internal.repository.postgresql.user import UserRepository
from internal.repository.postgresql.menu import MenuRepository
from internal.repository.postgresql.cart import CartRepository

class UserRepo:
    def __init__(self, pool):
        self.user = UserRepository(pool)
        self.menu = MenuRepository(pool)
        self.cart = CartRepository(pool)