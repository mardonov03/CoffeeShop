from internal.core.logging import logger
from internal.models import menu as model
from typing import List

class MenuRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create_category(self, category: model.CategoryCreate):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO category (name) VALUES ($1)", category.name)
        except Exception as e:
            logger.error(f"[create_category error]: {e}")

    async def get_all_categories(self) -> List[model.CategoryInfo]:
        try:
            async with self.pool.acquire() as conn:
                records = await conn.fetch("SELECT * FROM category")
                return [model.CategoryInfo(**dict(r)) for r in records]
        except Exception as e:
            logger.error(f"[get_all_categories error]: {e}")
            return []

    async def create_product(self, product: model.ProductCreate):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO product (name, info, price, volume_ml, categoryid) VALUES ($1, $2, $3, $4, $5)", product.name, product.info, product.price, product.volume_ml, product.category_id)
        except Exception as e:
            logger.error(f"[create_product error]: {e}")

    async def get_products_by_category(self, category_id: int) -> List[model.ProductInfo]:
        try:
            async with self.pool.acquire() as conn:
                records = await conn.fetch("""
                    SELECT * FROM product WHERE categoryid = $1
                """, category_id)
                return [model.ProductInfo(**dict(r)) for r in records]
        except Exception as e:
            logger.error(f"[get_products_by_category error]: {e}")
            return []

    async def delete_product(self, product_id: int):
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute("DELETE FROM product WHERE id = $1", product_id)
                if result == 'DELETE 0':
                    logger.error(f"[delete_product error]: No product found with id {product_id}")
        except Exception as e:
            logger.error(f"[delete_product error]: {e}")

    async def patch_product(self, product_id: int, product_update: model.ProductUpdate):
        try:
            updates = []
            params = []

            if product_update.name:
                updates.append("name = $1")
                params.append(product_update.name)
            if product_update.info:
                updates.append("info = $2")
                params.append(product_update.info)
            if product_update.price:
                updates.append("price = $3")
                params.append(product_update.price)
            if product_update.volume_ml:
                updates.append("volume_ml = $4")
                params.append(product_update.volume_ml)
            if product_update.category_id:
                updates.append("categoryid = $5")
                params.append(product_update.category_id)

            if updates:
                query = f"UPDATE product SET {', '.join(updates)} WHERE id = ${len(params) + 1}"
                params.append(product_id)
                async with self.pool.acquire() as conn:
                    await conn.execute(query, *params)
        except Exception as e:
            logger.error(f"[patch_product error]: {e}")

    async def patch_category(self, category_id: int, category_update: model.CategoryUpdate):
        try:
            if category_update.name:
                async with self.pool.acquire() as conn:
                    await conn.execute("UPDATE category SET name = $1 WHERE id = $2", category_update.name, category_id)
        except Exception as e:
            logger.error(f"[patch_category error]: {e}")