import uvicorn
from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from api.v1 import routers as v1_routers
from core.config import settings


def init_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    application.include_router(v1_routers, prefix=settings.API_V1_STR)

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return application


app = init_application()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next) -> Response:
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# Run Fast API app
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
