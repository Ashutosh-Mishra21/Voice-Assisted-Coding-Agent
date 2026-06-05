from fastapi import FastAPI

from backend.api.routes.health import (
    router as health_router,
)

from backend.api.routes.agent import (
    router as agent_router,
)

from backend.config.settings import (
    settings,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(health_router)

app.include_router(agent_router)


@app.get("/")
def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
