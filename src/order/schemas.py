from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    first_name: str
    last_name: str
    city: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True
