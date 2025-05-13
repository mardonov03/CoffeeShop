from internal.repository.postgresql.orders import OrdersRepossitory
from internal.service.user import UserService

class OrdersService:
    def __init__(self, pool, user_service: UserService):
        self.repo=OrdersRepossitory(pool)
        self.user_service=user_service

    async def test(self):
        return await self.repo.test2()