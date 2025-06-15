from fastapi import APIRouter
from .users import router as users_router
from .events import router as events_router
from .games import router as games_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(games_router,  prefix="/games",  tags=["Games"])
# add more include_router() lines as you create more blueprints
