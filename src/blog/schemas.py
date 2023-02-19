from datetime import datetime
from pydantic import BaseModel


class News(BaseModel):
    title: str
    content: str
    available: bool
    created_at: datetime
    category_id: int

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
