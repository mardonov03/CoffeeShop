from internal.repository.redis.menu import RedisMenuRepository
from internal.repository.postgresql.menu import MenuRepository
from internal.core.logging import logger
from fastapi import HTTPException
from internal.models import menu as model
from fastapi import Depends
from internal.service.user import UserService
from internal import dependencies

class MenuService:
    def __init__(self, pool, redis_pool, service: UserService = None):
        from internal import dependencies
        if service is None:
            service = dependencies.get_user_service()
        self.psql_repo = MenuRepository(pool)
        self.redis_repo = RedisMenuRepository(redis_pool)
        self.user_service = service

    async def create_category(self, category: model.CategoryCreate, gmail: str):
        try:
            is_admin = await self.user_service.is_admin(gmail)
            if is_admin:
                await self.psql_repo.create_category(category)
                return {"status": "ok", "message": "Category created successfully"}
        except Exception as e:
            logger.error(f"[create_category error]: {e}")
            raise HTTPException(status_code=500, detail="Error creating category")

    async def get_all_categories(self):
        try:
            categories = await self.psql_repo.get_all_categories()
            return {"status": "ok", "categories": categories}
        except Exception as e:
            logger.error(f"[get_all_categories error]: {e}")
            return {"status": "error", "message": "Error fetching categories"}

    async def create_product(self, product: model.ProductCreate, gmail: str):
        try:
            is_admin = await self.user_service.is_admin(gmail)
            if is_admin:
                await self.psql_repo.create_product(product)
                return {"status": "ok", "message": "Product created successfully"}
        except Exception as e:
            logger.error(f"[create_product error]: {e}")
            raise HTTPException(status_code=500, detail="Error creating product")

    async def get_products_by_category(self, category_id: int):
        try:
            products = await self.psql_repo.get_products_by_category(category_id)
            return {"status": "ok", "products": products}
        except Exception as e:
            logger.error(f"[get_products_by_category error]: {e}")
            return {"status": "error", "message": "Error fetching products"}

    async def patch_product(self, product_id: int, product_update: model.ProductUpdate, gmail: str):
        try:
            is_admin = await self.user_service.is_admin(gmail)
            if is_admin:
                await self.psql_repo.patch_product(product_id, product_update)
                return {"status": "ok", "message": "Product updated successfully"}
        except Exception as e:
            logger.error(f"[patch_product error]: {e}")
            raise HTTPException(status_code=500, detail="Error updating product")

    async def patch_category(self, category_id: int, category_update: model.CategoryUpdate, gmail: str):
        try:
            is_admin = await self.user_service.is_admin(gmail)
            if is_admin:
                await self.psql_repo.patch_category(category_id, category_update)
                return {"status": "ok", "message": "Category updated successfully"}
        except Exception as e:
            logger.error(f"[patch_category error]: {e}")
            raise HTTPException(status_code=500, detail="Error updating category")

    async def delete_product(self, product_id: int, gmail: str):
        try:
            is_admin = await self.user_service.is_admin(gmail)
            if is_admin:
                await self.psql_repo.delete_product(product_id)
                return {"status": "ok", "message": "Product deleted successfully"}
        except Exception as e:
            logger.error(f"[delete_product error]: {e}")
            raise HTTPException(status_code=500, detail="Error deleting product")
