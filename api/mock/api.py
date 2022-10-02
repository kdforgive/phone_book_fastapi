from fastapi import APIRouter
from api.mock.endpoints.login import router as login_router
from api.mock.endpoints.user import router as user_router
from api.mock.endpoints.stats import router as stats_router

api_router = APIRouter()

api_router.include_router(login_router)
api_router.include_router(user_router)
api_router.include_router(stats_router)
