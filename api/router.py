from api.v1 import tests_router, chat_router, rags_router
from fastapi import APIRouter


router = APIRouter(prefix='/api/v1', )
router.include_router(chat_router)
router.include_router(tests_router)
router.include_router(rags_router)

