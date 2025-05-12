from fastapi import APIRouter, Depends
from internal import dependencies
from internal.models import cart
from internal.service.cart import CartService

router = APIRouter()

@router.get("/")
async def get_cart_products(cartid: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return await service.get_cart_products(cartid, current_user["sub"])

@router.post("/")
async def add_product(model: cart.AddProduct, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return await service.add_product(model, current_user["sub"])

@router.patch("/{id}")
async def edit_product(model: cart.EditCart, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return await service.edit_product(model, current_user["sub"])

@router.delete("/{id}")
async def delete_product(model: cart.DeleteProduct, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return await service.delete_product(model, current_user["sub"])

@router.delete("/")
async def delete_all_products(model: cart.Clear, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return await service.delete_all_products(model, current_user["sub"])
