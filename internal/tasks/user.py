from internal.tasks.task import celery
import asyncio
from internal.repository.postgresql.db import create_pool

@celery.task
def delete_user(gmail: str):
    async def wrapper():
        try:
            pool = await create_pool()
            from internal.repository.postgresql.user import UserRepository
            repo = UserRepository(pool)
            is_verified = await repo.is_verified(gmail)
            if not is_verified:
                await repo.delete_user_by_gmail(gmail)
            await pool.close()
        except Exception as e:
            print(f"[delete_user error]: {e}")
    asyncio.run(wrapper())
