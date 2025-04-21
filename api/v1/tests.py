from fastapi import APIRouter


router = APIRouter(prefix='/test', tags=['test'])


@router.get('/info')
def hello():
    return 'Hello, this is a test file.'


@router.get('/say_hello')
def say_hello():
    return 'HELLO'