from api.routes import router
from core.config import cfg
from core.exceptions import BaseHTTPException
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


app = FastAPI(
    docs_url="/swagger/" if cfg.DEBUG else None,
    redoc_url="/redoc/" if cfg.DEBUG else None,
)

app.include_router(router)


@app.exception_handler(BaseHTTPException)
async def http_exception_handler(
    request: Request,
    exc: BaseHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.get_response(),
    )
