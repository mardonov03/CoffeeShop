from pydantic import BaseModel, constr, conint
from internal.models import menu

import datetime
class GetCart(BaseModel):
    cartid: int
    userid: int
    added_time: datetime.timedelta
    items: list[menu.ProductInfo] | None = None

class AddItem:
    pass

class EditCart:
    pass

class DeleteItem:
    pass

class Clear:
    pass