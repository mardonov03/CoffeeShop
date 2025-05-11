from fastapi import APIRouter, Depends
from internal import dependencies
from internal.models import menu as model
from internal.service.cart import CartService

router = APIRouter()

@router.get("/")
async def get_cart_products(cartid: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return service.repo.get_cart_products(cartid, current_user["sub"])

@router.post("/")
async def add_product(productid: int, cartid: int, quantity: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return service.repo.add_product(productid, cartid, quantity, current_user["sub"])

@router.patch("/{id}")
async def edit_product(id: int, cartid: int, quantity: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return service.repo.edit_product(id, cartid, quantity, current_user["sub"])

@router.delete("/{id}")
async def delete_product(id: int, cartid: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return service.repo.delete_product(id, cartid, current_user["sub"])

@router.delete("/")
async def delete_all_products(cartid: int, current_user: dict = Depends(dependencies.get_current_user), service: CartService = Depends(dependencies.get_cart_service)):
    return service.repo.delete_all_products(cartid, current_user["sub"])
