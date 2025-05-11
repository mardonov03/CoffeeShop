from internal.core.logging import logger

class CartRepository:
    def __init__(self, pool):
        self.pool=pool

    async def get_cart_products(self, cartid: int, gmail: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[get_cart_products error]: {e}')

    async def add_product(self, cartid: int, productid: int, quantity: int, gmail: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[add_product error]: {e}')

    async def edit_product(self, cartid: int, productid: int, quantity: int, gmail: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[edit_product error]: {e}')

    async def delete_product(self, cartid: int, productid: int, gmail: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[delete_product error]: {e}')

    async def delete_all_products(self, cartid: int, gmail: str):
        try:
            pass
        except Exception as e:
            logger.error(f'[delete_all_products error]: {e}')