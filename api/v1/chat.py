from fastapi import APIRouter


router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/qa')
def chat_with_llm(query: str):
    return query

@router.get('/health')
def chat_with_kn():
    return {"status": "OK"}