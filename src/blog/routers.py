from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.blog import models
from src.blog.schemas import Category, News
from src.database import get_async_session

router = APIRouter()


@router.post("/category/")
async def create_category(category: Category, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(models.category).values(**category.dict())
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
            "details": None
        })


@router.get("/category/", response_model=None)
@cache(expire=60 * 5)
async def get_list_category(offset: int = 0, limit: int = 5, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(models.category).offset(offset).limit(limit))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/category/{id}")
@cache(expire=60 * 5)
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(models.category).where(models.category.c.id == category_id))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/news/{id}")
async def get_news(news_id: int, session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(select(models.news).where(models.news.c.id == news_id))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/news/")
@cache(expire=60 * 5)
async def get_list_news(offset: int = 0, limit: int = 5, session: AsyncSession = Depends((get_async_session))):
    try:
        result = await session.execute(select(models.news).offset(offset).limit(limit))
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/news/")
async def create_news(news: News, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(models.news).values(**news.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": news,
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.put("/news/{id}")
async def put_news(news_id: int, news: News, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(models.news).where(models.news.c.id == news_id).values(**news.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": news,
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.delete("/news/")
async def delete_news(news_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(models.news).where(models.news.c.id == news_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": f'news {news_id} was be delete',
            "detail": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
