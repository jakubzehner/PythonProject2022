from fastapi import APIRouter
from server import endpoints

router = APIRouter()
router.include_router(endpoints.user.router)
router.include_router(endpoints.entry.router)
router.include_router(endpoints.planned_entry.router)
router.include_router(endpoints.goal.router)
