from fastapi import FastAPI
from internal.repository.postgresql import db
from internal.core.logging import logger
from internal.api import user, auth, products, categories
from internal.repository.redis import db as redis_db

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(categories.router, prefix="/categories", tags=["Category"])
app.include_router(products.router, prefix="/products", tags=["Product"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])

@app.on_event('startup')
async def eventstart():
    try:
        app.state.pool = await db.create_pool()
        await db.init_db(app.state.pool)
        app.state.redis_pool = await redis_db.create_redis()
    except Exception as e:
        logger.error(f'[eventstart error]: {e}')

@app.on_event('shutdown')
async def shutdownevent():
    try:
        await app.state.pool.close()
    except Exception as e:
        logger.error(f'[shutdownevent error]: {e}')

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CoffeeShop API",
        version="1.0.0",
        description="Документация API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
