from internal.core.logging import logger
from internal.models import menu as model
from typing import List
from fastapi import HTTPException

class MenuRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create_product(self, product: model.ProductCreate):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO product (name, info, price, volume_ml, categoryid) VALUES ($1, $2, $3, $4, $5)", product.name, product.info, product.price, product.volume_ml, product.categoryid)
        except Exception as e:
            logger.error(f"[create_product error]: {e}")

    async def get_all_products(self) -> list[model.ProductInfo]:
        try:
            async with self.pool.acquire() as conn:
                products = await conn.fetch("SELECT p.productid, p.name,p.info, p.price, p.volume_ml, p.categoryid, c.categoryname FROM product p LEFT JOIN category c ON p.categoryid = c.categoryid")
                if products:
                    return [model.ProductInfo(**dict(r)) for r in products]
        except Exception as e:
            logger.error(f"[get_all_products error]: {e}")
            return []

    async def get_products_by_id(self, prod_id: int) -> model.ProductInfo:
        try:
            async with self.pool.acquire() as conn:
                product = await conn.fetchrow("SELECT p.productid, p.name,p.info, p.price, p.volume_ml, p.categoryid, c.categoryname FROM product p LEFT JOIN category c ON p.categoryid = c.categoryid WHERE productid = $1", prod_id)
                if product:
                    return model.ProductInfo(**dict(product))
        except Exception as e:
            logger.error(f"[get_products_by_id error]: {e}")

    async def delete_product(self, product_id: int):
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute("DELETE FROM product WHERE productid = $1", product_id)
                if result == 'DELETE 0':
                    logger.error(f"[delete_product error]: No product found with productid {product_id}")
                    raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
        except Exception as e:
            logger.error(f"[delete_product error]: {e}")

    async def patch_product(self, product_id: int, product_update: model.ProductUpdate):
        try:
            updates = []
            params = []

            if product_update.name:
                updates.append("name = ${}".format(len(params) + 1))
                params.append(product_update.name)
            if product_update.info:
                updates.append("info = ${}".format(len(params) + 1))
                params.append(product_update.info)
            if product_update.price:
                updates.append("price = ${}".format(len(params) + 1))
                params.append(product_update.price)
            if product_update.volume_ml:
                updates.append("volume_ml = ${}".format(len(params) + 1))
                params.append(product_update.volume_ml)
            if product_update.categoryid:
                updates.append("categoryid = ${}".format(len(params) + 1))
                params.append(product_update.categoryid)

            params.append(product_id)

            if updates:
                query = f"UPDATE product SET {', '.join(updates)} WHERE productid = ${len(params)}"
                async with self.pool.acquire() as conn:
                    result = await conn.execute(query, *params)
                    if result == "UPDATE 0":
                        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

        except Exception as e:
            logger.error(f"[patch_product error]: {e}")
            raise

    async def create_category(self, category: model.CategoryCreate):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO category (categoryname) VALUES ($1)", category.categoryname)
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