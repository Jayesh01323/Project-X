from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import create_db_and_tables
from app.providers.registry import ProviderRegistry
from app.core.provider_factory import create_provider

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and provider registry on startup."""
    create_db_and_tables()
    app.state.provider_registry = ProviderRegistry
    app.state.active_provider = create_provider(settings.ACTIVE_PROVIDER)
    print(f"[OK] {settings.PROJECT_NAME} v{settings.VERSION} started successfully")
    print("[OK] Database initialized")
    count = len(ProviderRegistry.list_providers())
    print(f"[OK] Provider registry initialized with {count} provider(s)")
    print("[OK] API documentation available at /docs")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.VERSION
    }
