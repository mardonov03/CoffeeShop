from internal.repository.redis.menu import RedisMenuRepository
from internal.repository.postgresql.menu import MenuRepository
from internal.core.logging import logger
from fastapi import HTTPException
from internal.models import menu as model
from internal.service.user import UserService

class MenuService:
    def __init__(self, pool, redis_pool, user_service: UserService):
        self.psql_repo = MenuRepository(pool)
        self.redis_repo = RedisMenuRepository(redis_pool)
        self.user_service = user_service

    async def create_category(self, category: model.CategoryCreate, gmail: str):
        is_admin = await self.user_service.is_admin(gmail)
        if is_admin:
            await self.psql_repo.create_category(category)
            return {"status": "ok", "message": "Category created successfully"}

    async def get_all_categories(self):
        categories = await self.psql_repo.get_all_categories()
        return {"status": "ok", "categories": categories}

    async def create_product(self, product: model.ProductCreate, gmail: str):
        is_admin = await self.user_service.is_admin(gmail)
        if is_admin:
            await self.psql_repo.create_product(product)
            return {"status": "ok", "message": "Product created successfully"}

    async def get_products_by_id(self, prod_id: int):
        product = await self.psql_repo.get_products_by_id(prod_id)
        return {"status": "ok", "product": product}

    async def get_all_products(self):
        products = await self.psql_repo.get_all_products()
        return {"status": "ok", "products": products}

    async def patch_product(self, product_id: int, product_update: model.ProductUpdate, gmail: str):
        is_admin = await self.user_service.is_admin(gmail)
        if is_admin:
            await self.psql_repo.patch_product(product_id, product_update)
            return {"status": "ok", "message": "Product updated successfully"}

    async def delete_product(self, product_id: int, gmail: str):
        is_admin = await self.user_service.is_admin(gmail)
        if is_admin:
            await self.psql_repo.delete_product(product_id)
            return {"status": "ok", "message": "Product deleted successfully"}
