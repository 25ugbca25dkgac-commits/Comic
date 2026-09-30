from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "AI comic story and "
        "illustration generator."
    ),
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),
    name="static",
)


app.include_router(
    router
)


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": settings.app_name,
        "image_backend": settings.image_backend,
        "panels": settings.comic_panels,
    }