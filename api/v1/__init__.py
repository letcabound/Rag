from api.v1.tests import router as tests_router
from api.v1.chat import router as chat_router
from api.v1.rags import router as rags_router

__all__ = [
    'tests_router',
    'chat_router',
    'rags_router'
]