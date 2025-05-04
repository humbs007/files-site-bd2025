# backend/app/api/endpoints/search/__init__.py

from fastapi import APIRouter
from .option1 import router as option1_router
from .option2 import router as option2_router

router = APIRouter()
router.include_router(option1_router, prefix="/option1")
router.include_router(option2_router, prefix="/option2")
