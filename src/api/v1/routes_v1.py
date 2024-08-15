from fastapi import APIRouter
from api.v1.bot_user.auth.controller import router as bot_user_auth_router
from api.v1.bot_user.job.controller import router as bot_user_job_router


router_v1 = APIRouter(prefix="/v1")


routers = [
    (bot_user_auth_router, "/auth", ["Авторизация"]),
    (bot_user_job_router, "/job", ["Работа"]),
]

for router in routers:
    router_v1.include_router(router[0], prefix=router[1], tags=router[2])
