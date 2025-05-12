from internal.core.logging import logger
from internal.models import cart
from internal.models import menu

class CartRepository:
    def __init__(self, pool):
        self.pool = pool

    async def get_cart_products(self, cartid: int):
        try:
            async with self.pool.acquire() as conn:
                cart_row = await conn.fetchrow("SELECT * FROM cart WHERE cartid = $1", cartid)
                cart_products = await conn.fetch("SELECT p.productid, p.name, p.info, p.price, p.volume_ml, cp.quantity FROM cart_products cp JOIN product p ON cp.productid = p.productid WHERE cp.cartid = $1", cartid)

                products = [menu.ProductInfo(**dict(row)) for row in cart_products]

                return cart.GetCart(cartid=cart_row['cartid'], userid=cart_row['userid'], added_time=cart_row['added_time'], products=products)
        except Exception as e:
            logger.error(f'[get_cart_products error]: {e}')
            raise

    async def add_product(self, model: cart.AddProduct):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO cart_products (cartid, productid, quantity) VALUES ($1, $2, $3)", model.cartid, model.productid, model.quantity)
        except Exception as e:
            logger.error(f'[add_product error]: {e}')
            raise

    async def edit_product(self, model: cart.EditCart):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("UPDATE cart_products SET productid = $1, quantity = $2 WHERE cartid = $3", model.productid, model.quantity, model.cartid)
        except Exception as e:
            logger.error(f'[edit_product error]: {e}')
            raise

    async def delete_product(self, model: cart.DeleteProduct):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM cart_products WHERE productid = $1 AND cartid = $2", model.productid, model.cartid)
        except Exception as e:
            logger.error(f'[delete_product error]: {e}')
            raise

    async def delete_all_products(self, model: cart.Clear):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM cart_products WHERE cartid = $1", model.cartid)
        except Exception as e:
            logger.error(f'[delete_all_products error]: {e}')
            raise
