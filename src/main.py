from redis import asyncio as aioredis
import uvicorn
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.blog.routers import router as blog_router
from src.store.routers import router as store_router
from src.order.routers import router as order_router
from src.tasks.router import router as celery_router

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.router.include_router(
    blog_router,
    prefix="/blog",
    tags=["Blog"]
)
app.router.include_router(
    store_router,
    prefix="/store",
    tags=["Store"])

app.router.include_router(
    order_router,
    prefix="/order",
    tags=["Order"])

app.router.include_router(celery_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://redis:6379/0", encodings="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
