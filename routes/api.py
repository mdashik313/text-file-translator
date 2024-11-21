from fastapi import APIRouter
from src.endpoints import paths

router = APIRouter()
router.include_router(paths.router)

