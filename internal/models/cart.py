from pydantic import BaseModel, constr, conint
from internal.models import menu
import datetime

class CartProductInfo(BaseModel):
    product: menu.ProductInfo
    quantity: int

class GetCart(BaseModel):
    cartid: int
    userid: int
    added_time: datetime.datetime
    products: list[CartProductInfo] | None = None

class AddProduct(BaseModel):
    productid: int
    cartid: int
    quantity: conint(gt=0)

class EditCart(BaseModel):
    productid: int
    cartid: int
    quantity: conint(gt=0)

class DeleteProduct(BaseModel):
    productid: int
    cartid: int

class Clear(BaseModel):
    cartid: int