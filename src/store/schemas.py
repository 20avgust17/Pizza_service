from datetime import datetime


from pydantic import BaseModel


class CategoryProduct(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    title: str
    content: str
    weight: int
    price: int
    available: bool
    created_at: datetime
    category_id: int

    class Config:
        orm_mode = True


class ProductBasket(BaseModel):
    product: int
    quantity: int


class Basket(BaseModel):
    product: int
    quantity: int

    class Config:
        orm_mode = True


class Data(BaseModel):
    x: int
    y: int

    class Config:
        orm_mode = True


