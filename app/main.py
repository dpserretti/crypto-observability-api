from fastapi import FastAPI

from app.api.routes.crypto import router as crypto_router
from app.api.routes.health import router as health_router
from app.core.lifespan import lifespan

app = FastAPI(
    title="Crypto Observability API",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(crypto_router)
