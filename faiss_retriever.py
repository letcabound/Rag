from langchain_huggingface import HuggingFaceEmbeddings
import torch
import config
import faiss
from doc_parser import DocParser

from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from typing import List, Tuple
from langchain_core.documents import Document


class FaissRetriever:
    def __init__(self, model_path: str, kn_data: list[Document]):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_path,
                                                model_kwargs={'device': 'cpu'},
                                                encode_kwargs={'normalize_embeddings': True}
                            )
        embedding_dim = len(self.embeddings.embed_query("hello world"))
        self.vector_store = FAISS(embedding_function=self.embeddings,
                                  index=faiss.IndexFlatL2(embedding_dim),
                                  docstore=InMemoryDocstore(),
                                  index_to_docstore_id={},)
        self.vector_store.add_documents(kn_data)
        del self.embeddings
        torch.cuda.empty_cache()

    def get_top_k(self, query: str, k: int = 2) -> List[Document]:
        return self.vector_store.similarity_search(query, k)

    def get_vector_store(self):
        return self.vector_store


if __name__ == '__main__':
    kn_path = config.PATH_FILE_KN
    model_path = config.PATH_BGE_M3
    kn_data = DocParser(file_path=kn_path).parse_and_split()
    retriever = FaissRetriever(model_path=model_path, kn_data=kn_data)
    print(retriever.get_top_k("地理学是什么"))