from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Table, MetaData

from src.auth.models import user

metadata = MetaData()

orders = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user', ForeignKey(user.c.id)),
    Column('total_price', Integer),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('city', String, nullable=False),
    Column('address', String, nullable=False),
    Column('created_at', TIMESTAMP),
)
