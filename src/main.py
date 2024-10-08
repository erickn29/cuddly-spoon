import uvicorn

from api.routes import router
from core.config import cfg
from core.exceptions import BaseHTTPException
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


app = FastAPI(
    docs_url="/swagger/" if cfg.DEBUG else None,
    redoc_url="/redoc/" if cfg.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.ALLOWED_HOSTS,
    allow_credentials=cfg.ALLOWED_CREDENTIALS,
    allow_methods=cfg.get_list_allowed_methods,
    allow_headers=cfg.ALLOWED_HEADERS,
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
