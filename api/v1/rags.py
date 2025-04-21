from fastapi import APIRouter
from service import RagQaService
from loguru import logger


router = APIRouter(prefix='/rags', tags=['rags'])


@router.get('/health')
def check_health():
    return {"status": "OK"}


@router.post('/geology')
def rags_qa(query: str):
    logger.info(f"请求参数，query: {query}")
    kn_file_name = "地理知识科普.pdf"

    try:
        server = RagQaService(kn_file_name=kn_file_name, rerank_by_model=True)
        response = server.invoke(query)
        return {'code': 0, 'msg': response}
    except Exception as e:
        return {"code": -1, "msg":str(e)}
