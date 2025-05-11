from pydantic import BaseModel, constr, conint

class ProductCreate(BaseModel):
    name: constr(min_length=1)
    info: str | None = None
    price: conint(ge=0)
    volume_ml: conint(ge=0)
    categoryid: conint(ge=1) = None

class ProductInfo(BaseModel):
    productid: int
    name: str
    info: str | None = None
    price: int
    volume_ml: float
    categoryid: int | None = None
    categoryname: str | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    info: str | None = None
    price: int | None = None
    volume_ml: float | None = None
    categoryid: int | None = None

class CategoryCreate(BaseModel):
    categoryname: constr(min_length=1)

class CategoryUpdate(BaseModel):
    categoryname: str | None = None

class CategoryInfo(BaseModel):
    id: conint(ge=1)
    categoryname: str
