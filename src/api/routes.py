from api.v1.routes_v1 import router_v1
from fastapi import APIRouter


router = APIRouter(prefix="/api")
router.include_router(router_v1)
