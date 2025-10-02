from contextlib import asynccontextmanager
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.core.config import settings
from app.api.graphql import schema
from infrastructure.database.session import init_db


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
    description="FastAPI with DDD Architecture - GraphQL API",
    lifespan=lifespan,
)

# GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


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
