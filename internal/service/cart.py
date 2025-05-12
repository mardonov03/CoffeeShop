from internal.service.user import UserService
from internal.models import cart
from internal.repository.postgresql.cart import CartRepository
from fastapi import HTTPException

class CartService:
    def __init__(self, pool, service: UserService):
        self.repo = CartRepository(pool)
        self.user_service = service

    async def get_cart_products(self, cartid: int, gmail: str):
        result = await self.user_service.is_cart_belongs(gmail, cartid)

        if not result:
            raise HTTPException(status_code=403, detail="You do not have permission")
        try:
            return await self.repo.get_cart_products(cartid)
        except Exception:
            raise HTTPException(status_code=500, detail="Error while receiving the cart")

    async def add_product(self, model: cart.AddProduct, gmail: str):
        result = await self.user_service.is_cart_belongs(gmail, model.cartid)

        if not result:
            raise HTTPException(status_code=403, detail="You do not have permission")
        try:
            await self.repo.add_product(model)
            return {"status": 'ok'}
        except Exception:
            raise HTTPException(status_code=500, detail="Error adding product")

    async def edit_product(self, model: cart.EditCart, gmail: str):
        result = await self.user_service.is_cart_belongs(gmail, model.cartid)

        if not result:
            raise HTTPException(status_code=403, detail="You do not have permission")
        try:
            await self.repo.edit_product(model)
            return {"status": 'ok'}
        except Exception:
            raise HTTPException(status_code=500, detail="Error while editing product")

    async def delete_product(self, model: cart.DeleteProduct, gmail: str):
        result = await self.user_service.is_cart_belongs(gmail, model.cartid)

        if not result:
            raise HTTPException(status_code=403, detail="You do not have permission")
        try:
            await self.repo.delete_product(model)
            return {"status": 'ok'}
        except Exception:
            raise HTTPException(status_code=500, detail="Error removing product")

    async def delete_all_products(self, model: cart.Clear, gmail: str):
        result = await self.user_service.is_cart_belongs(gmail, model.cartid)

        if not result:
            raise HTTPException(status_code=403, detail="You do not have permission")
        try:
            await self.repo.delete_all_products(model)
            return {"status": 'ok'}
        except Exception:
            raise HTTPException(status_code=500, detail="Error emptying recycle bin")
