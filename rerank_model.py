import config

import torch
from sentence_transformers.cross_encoder import CrossEncoder
from langchain_core.documents import Document

from doc_parser import DocParser
from faiss_retriever import FaissRetriever

CUDA_DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


def gpu_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

class Reranker(object):
    def __init__(self, model_path: str):
        self.model = CrossEncoder(model_path, device=CUDA_DEVICE)

    def predict(self, query: str, docs: list[Document]) -> list[str]:
        docs = [doc.page_content for doc in docs]
        scores = self.model.predict([[query, doc] for doc in docs])
        response = [doc for score, doc in sorted(zip(scores, docs), reverse=True, key=lambda x: x[0])]
        gpu_gc()
        return response


if __name__ == "__main__":
    kn_path = config.PATH_FILE_KN
    model_path = config.PATH_BGE_M3
    rerank_model_path = config.PATH_BGE_RERANKER

    kn_data = DocParser(file_path=kn_path).parse_and_split()
    retriever = FaissRetriever(model_path=model_path, kn_data=kn_data)
    reRanker = Reranker(rerank_model_path)

    question = "地理学是什么"
    retriever_result = retriever.get_top_k(question)
    print('检索结果：', [res.page_content for res in retriever_result])
    print('rerank结果：', reRanker.predict(question, retriever_result))