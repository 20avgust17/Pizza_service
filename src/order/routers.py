from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.tasks import send_email_order
from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.order import models
from src.order.schemas import Order
from src.store.models import basket, product

router = APIRouter()


@router.post("/order/")
async def create_order(order: Order, user: User = Depends(current_user),
                       session: AsyncSession = Depends((get_async_session))):
    try:
        total_price = 0
        result = await session.execute(
            select(basket.c.quantity, product.c.price).join(product, product.c.id == basket.c.product))
        for query in result.all():
            total_price += query.quantity * query.price
        send_email_order.delay(user.username, user.email)

        await session.execute(insert(models.orders).values(**order.dict(), total_price=total_price, user=user.id))
        await session.execute(delete(basket).where(basket.c.user == user.id))
        await session.commit()
        return {
            "status": "success",
            "data": order,
            "detail": "basket_remove",
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "basket_remove error"
        })


@router.get("/order/")
@cache(expire=30)
async def create_order(offset: int = 0, limit: int = 5, user: User = Depends(current_user),
                       session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(
            select(models.orders).where(models.orders.c.user == user.id).offset(offset).limit(limit))
        return {
            "status": "success",
            "data": result.all(),
            "detail": "basket_remove",
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "basket_remove error"
        })
