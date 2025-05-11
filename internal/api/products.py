from fastapi import APIRouter, Depends
from internal import dependencies
from internal.models import menu as model

router = APIRouter()

@router.post("/")
async def create_product(menu: model.ProductCreate ,service = Depends(dependencies.get_menu_service), current_user: dict = Depends(dependencies.get_current_user)):
    return await service.create_product(menu, current_user['sub'])

@router.get("/")
async def get_all_products(service = Depends(dependencies.get_menu_service)):
    return await service.get_all_products()

@router.get("/{id}")
async def get_products_by_id(id: int, service = Depends(dependencies.get_menu_service)):
    return await service.get_products_by_id(id)

@router.patch("/{id}")
async def patch_product(id: int, menu: model.ProductUpdate, service = Depends(dependencies.get_menu_service), current_user: dict = Depends(dependencies.get_current_user)):
    return await service.patch_product(id, menu, current_user["sub"])

@router.delete("/{id}")
async def delete_product(id: int, service = Depends(dependencies.get_menu_service), current_user: dict = Depends(dependencies.get_current_user)):
    return await service.delete_product(id, current_user["sub"])
