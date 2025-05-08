from internal.repository.postgresql.user import UserRepository

class UserService:
    def __init__(self, pool):
        self.repo = UserRepository(pool)

    async def get_user_count(self):
        return await self.repo.get_user_count()

    async def get_me(self, username):
        return await self.repo.get_user_data(username)