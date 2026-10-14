"""FastAPI User Service Application Entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.user_controller import router as user_router
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    try:
        init_db()
    except Exception as exc:
        print(f"Warning: Database initialization deferred or failed: {exc}")
    yield


app = FastAPI(
    title="Poll System - User Service",
    description="Microservice responsible for managing system users and registration status.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers under /api/v1
app.include_router(user_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {
        "service": settings.SERVICE_NAME,
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "user-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
