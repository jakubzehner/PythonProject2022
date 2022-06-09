from fastapi import APIRouter
from server import endpoints

# Zbieranie "routerów" ze wszystkich endpointów do jednego, aby dało się w elegancki sposób uruchomić w mainie

router = APIRouter()
router.include_router(endpoints.user.router)
router.include_router(endpoints.entry.router)
router.include_router(endpoints.planned_entry.router)
router.include_router(endpoints.goal.router)
