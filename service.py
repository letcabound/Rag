from config import cfg

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document
from loguru import logger

from doc_parser import DocParser
from retriever_faiss import FaissRetriever
from rerank_model import Reranker


class RagQaService(object):
    def __init__(self, kn_file_name: str,
                 rerank_by_model: bool = True,
                 ):
        self.kn_file_name = kn_file_name
        self.retriever_model_path = cfg.PATH_BGE_M3
        self.llm_api_key = cfg.ZHIPU_API_KEY
        self.llm_model_name = cfg.ZHIPU_MODEL_NAME
        self.rerank_by_model = cfg.RERANK_BY_MODEL
        self.rerank_model_path = cfg.PATH_BGE_RERANKER

    def get_kn_by_query(self, query: str) -> str:
        doc_parser = DocParser(file_name=self.kn_file_name)
        doc_parser.parse_all_pages(chunk_size=512, min_seq_len=6)
        kn_data = [Document(page_content=doc) for doc in doc_parser.data]

        retriever = FaissRetriever(model_path=self.retriever_model_path, kn_data=kn_data)
        retriever_data = retriever.get_top_k(query, k=2)
        logger.info(f"检索结果: {[data.page_content for data in retriever_data]}")

        if self.rerank_by_model:
            reranker = Reranker(self.rerank_model_path)
            rerank_result = reranker.predict(query, retriever_data)
            logger.info(f"重排结果: {rerank_result}")
            return "\n\n".join(rerank_result)
        else:
            # 通过 rrf算法，返回 混合检索召回重排 的结果。【待实现】
            return "\n\n".join([res.page_content for res in retriever_data])


    def invoke(self, query) -> str:
        llm = ChatZhipuAI(
            model=cfg.ZHIPU_MODEL_NAME,
            temperature=0.5,
            api_key=cfg.ZHIPU_API_KEY
        )
        doc_str = self.get_kn_by_query(query)

        prompt = '''
            根据提供的文本内容来回答用户的问题，你的回答只能依据输入的文本内容，禁止胡乱回答。
            输入的文本内容为:{doc_str}
            '''.format(doc_str=doc_str)

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=query),
        ]

        response = llm.invoke(messages)
        return response.content


if __name__ == '__main__':
    user_question = "现代地理学广泛使用的技术手段有哪些"
    kn_file_name = "地理知识科普.pdf"

    server = RagQaService(kn_file_name=kn_file_name, rerank_by_model=True)
    response = server.invoke(user_question)

    print('='*10, '问答结果', '='*10)
    print('用户提问:', user_question)
    print('模型回答:', response)









