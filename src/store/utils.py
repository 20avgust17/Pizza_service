from fastapi import Depends
from sqlalchemy import delete, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.order.schemas import Order
from src.store import models
from src.store.models import basket, product
from src.store.schemas import Basket


async def delete_product_basket(id: int, user: User = Depends(current_user),
                                session: AsyncSession = Depends((get_async_session))):
    stmt = delete(models.basket).where(models.basket.c.user == user.id,
                                       models.basket.c.product == id)
    await session.execute(stmt)
    await session.commit()
    return id


async def create_or_update(basket: Basket, user: User = Depends(current_user),
                           session: AsyncSession = Depends((get_async_session))):
    result = await session.execute(
        select(models.basket).where(models.basket.c.user == user.id, models.basket.c.product == basket.product))
    if result.scalar():
        stmt = update(models.basket).where(models.basket.c.user == user.id,
                                           models.basket.c.product == basket.product).values(**basket.dict(), user=user.id)
        await session.execute(stmt)
        await session.commit()
        return basket
    else:
        stmt = insert(models.basket).values(**basket.dict(), user=user.id)
        await session.execute(stmt)
        await session.commit()
        return basket


async def create_order(user: User = Depends(current_user),
                  session: AsyncSession = Depends((get_async_session))):

    subq = select(models.product)
    stmt = select(basket).join(subq, basket.c.product == product.c.id)
    print(stmt)
    result = await session.execute(stmt)
    for query in result.all():
        print(query.quantity * query.price)




