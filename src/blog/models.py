from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Table

from src.database import metadata

category = Table(
    "category",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
)

news = Table(
    'news',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String),
    Column('content', String),
    Column('available', Boolean),
    Column('created_at', TIMESTAMP),
    Column('category_id', Integer, ForeignKey(category.c.id)),
)

