from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from infrastructure.database.session import init_db
from interfaces.api.client_routes import router as client_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events pour initialiser la base de données."""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI with DDD Architecture - Client Management API",
    lifespan=lifespan,
)

# Include routers
app.include_router(client_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Memory Business API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
