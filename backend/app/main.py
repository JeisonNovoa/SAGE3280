from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.routes import upload, patients, stats, export, controls, alerts, admin, rules

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(controls.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(rules.router, prefix="/api")  # Configurable rules management


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on startup.
    """
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.VERSION} iniciado")
    print(f"📊 Base de datos: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'SQLite'}")
    print(f"🔗 Documentación API: http://{settings.API_HOST}:{settings.API_PORT}/api/docs")
    print(f"🌐 CORS Origins: {settings.CORS_ORIGINS}")


@app.get("/")
async def root():
    """
    Root endpoint - API info.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs": "/api/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
