# from api.v1.bot_user.job.controller import router as bot_user_job_router
# from api.v1.bot_user.management.controller import router as bot_user_management_router
from api.v1.bot_user.crud.controller import router as bot_user_crud
from api.v1.user.controller import router as user_router
from fastapi import APIRouter


router_v1 = APIRouter(prefix="/v1")


routers = [
    # (bot_user_job_router, "/bot/job", ["Работа"]),
    # (bot_user_management_router, "/bot/management", ["Управление"]),
    (user_router, "/user", ["Пользователь"]),
    (bot_user_crud, "/bot", ["Бот"]),
]

for router in routers:
    router_v1.include_router(router[0], prefix=router[1], tags=router[2])
