from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.auth.base_config import current_user
from src.auth.models import User

from src.database import get_async_session
from src.store import models

from src.store.schemas import Product, CategoryProduct, Basket, Data
from src.store.utils import delete_product_basket, create_or_update

router = APIRouter()


@router.post("/category_product/")
async def create_category_product(category: CategoryProduct, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(models.category_product).values(**category.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": category,
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "create_category_product error"
        })


@router.get("/category_product/", response_model=None)
@cache(expire=60 * 5)
async def get_list_category_product(offset: int = 0, limit: int = 5,
                                    session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(models.category_product).offset(offset).limit(limit))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "get_list_category_product error"
        })


@router.get("/category_product/{id}")
async def get_category_product(category_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(
            select(models.category_product).where(models.category_product.c.id == category_id))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "get_category_product error"
        })


@router.get("/product/{id}")
async def get_product(product_id: int, session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(select(models.product).where(models.product.c.id == product_id))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "get_product error"
        })


@router.get("/product/")
@cache(expire=60 * 5)
async def get_list_product(offset: int = 0, limit: int = 5, session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(select(models.product).offset(offset).limit(limit))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "get_list_product error"
        })


@router.post("/product/")
async def create_product(product: Product, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(models.product).values(**product.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": product,
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "create_product error"
        })


@router.put("/product/{id}")
async def put_product(product_id: int, product: Product, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(models.product).where(models.product.c.id == product_id).values(**product.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": product,
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "put_product error"
        })


@router.delete("/product/")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(models.product).where(models.product.c.id == product_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": f'news {product_id} was be delete',
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "delete_product error"
        })


@router.post("/basket_add/")
async def get_add(basket: Basket, user: User = Depends(current_user),
                  session: AsyncSession = Depends((get_async_session))):
    result = await create_or_update(basket, user=user, session=session)
    try:
        return {
            "status": "success",
            "data": basket,
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "get_add error"
        })


@router.delete("/basket_remove/{id}")
async def remove_basket(id: int, user: User = Depends(current_user),
                        session: AsyncSession = Depends((get_async_session))):
    result = await delete_product_basket(id, user=user, session=session)
    try:
        return {
            "status": "success",
            "data": f"Product {id} - has been delete",
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "remove_basket error"
        })


@router.get("/basket_all/")
async def basket_list(user: User = Depends(current_user),
                      session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(select(models.basket).where(models.basket.c.user == user.id))
        return {
            "status": "success",
            "data": result.all(),
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "basket_list error"
        })


@router.delete("/basket_remove_all/")
async def basket_remove_all(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(delete(models.basket).where(models.basket.c.user == user.id))
        await session.commit()

        return {
            "status": "success",
            "data": None,
            "detail": "basket_remove",
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "basket_remove error"
        })
