from pydantic import BaseModel, constr, conint
from typing import Optional

class CategoryCreate(BaseModel):
    name: constr(min_length=1)

class ProductCreate(BaseModel):
    name: constr(min_length=1)
    info: Optional[str] = None
    price: conint(ge=0)
    volume_ml: conint(ge=0)
    category_id: conint(ge=1)

class CategoryInfo(BaseModel):
    id: conint(ge=1)
    name: str

class ProductInfo(BaseModel):
    id: conint(ge=1)
    name: str
    info: Optional[str]
    price: conint(ge=0)
    volume_ml: conint(ge=0)
    category_id: conint(ge=1)
    category_name: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    info: Optional[str] = None
    price: Optional[int] = None
    volume_ml: Optional[float] = None
    category_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None