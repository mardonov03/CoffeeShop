from internal.tasks.task import celery
from internal.repository.postgresql.user import UserRepository
import asyncio

@celery.task
def delete_user(gmail: str, pool):
    async def wrapper():
        try:
            repo = UserRepository(pool)
            is_verified = await repo.is_verified(gmail)
            if not is_verified:
                await repo.delete_user_by_gmail(gmail)
        except Exception as e:
            print(f"[delete_user error]: {e}")

    asyncio.run(wrapper())
