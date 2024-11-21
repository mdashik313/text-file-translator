from fastapi import APIRouter
from src.endpoints import hello

router = APIRouter()
router.include_router(hello.router)
