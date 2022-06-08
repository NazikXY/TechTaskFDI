from fastapi import APIRouter
from .auth import router as auth_router
from .currencies import router as currencies_router

router = APIRouter(prefix='')

router.include_router(auth_router)
router.include_router(currencies_router)
