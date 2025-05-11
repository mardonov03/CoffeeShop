from internal.service.user import UserService
from internal.models import menu
from internal.repository.postgresql.cart import CartRepository

class CartService:
    def __init__(self, pool, service: UserService):
        self.repo=CartRepository(pool)
        self.user_service=service

    async def get_cart_products(self, cartid: int, gmail: str):
        return {"status": "test"}

    async def add_product(self, productid: int, cartid: int, quantity: int, gmail: str):
        pass

    async def edit_product(self, productid: int, cartid: int, quantity: int, gmail: str):
        pass

    async def delete_product(self, productid: int, cartid: int, gmail: str):
        pass

    async def delete_all_products(self, cartid: int, gmail: str):
        pass