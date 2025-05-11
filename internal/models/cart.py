from pydantic import BaseModel, constr, conint
from internal.models import menu

import datetime
class GetCart(BaseModel):
    cartid: int
    userid: int
    added_time: datetime.timedelta
    products: list[menu.ProductInfo] | None = None

class AddProduct:
    pass

class EditCart:
    pass

class DeleteProduct:
    pass

class Clear:
    pass