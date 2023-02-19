from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Table, MetaData

from src.auth.models import user

metadata = MetaData()

category_product = Table(
    "category_product",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(150), nullable=False),
)

product = Table(
    "product",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False),
    Column('content', String(500)),
    Column('weight', Integer, nullable=False),
    Column('price', Integer, nullable=False),
    Column('available', Boolean, nullable=False),
    Column('created_at', TIMESTAMP),
    Column('category_id', Integer, ForeignKey(category_product.c.id), nullable=False),
)

basket = Table(
    "basket",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user', Integer, ForeignKey(user.c.id)),
    Column('product', Integer, ForeignKey(product.c.id)),
    Column('quantity', Integer, nullable=False),
)
