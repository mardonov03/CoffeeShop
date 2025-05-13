from fastapi import APIRouter, Depends
from internal import dependencies
from internal.service.orders import OrdersService

router = APIRouter()

@router.get("/")
async def test(service: OrdersService = Depends(dependencies.get_orders_service)):
    return await service.test()