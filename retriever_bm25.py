import jieba

from doc_parser import DocParser

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

"""
工业上稀疏召回用es；
bm25默认按照 空格进行分词，所以在处理中文文本的时候需要 用jieba预处理一下。
"""
class BM25(object):

    def __init__(self, documents: list[str]):
        docs: list[Document] = []  # jieba分词后，用 空格 拼接后的数据
        org_docs: list[Document] = []  # 原始文档数据
        for idx, document in enumerate(documents):
            org_docs.append(Document(page_content=document, metedata={"source": idx}))
            line = document.strip("\n").strip()
            if line:
                docs.append(Document(page_content=" ".join(jieba.cut_for_search(line)),
                                     metadata={"source": idx}))
        self.retriever = BM25Retriever.from_documents(docs)
        self.org_docs = org_docs

    def get_bm_top_k(self, query: str, k: int = 2) -> list[Document]:
        self.retriever.k = k
        query = " ".join(jieba.cut_for_search(query))
        retriever_docs = self.retriever.invoke(query)
        return [self.org_docs[doc.metadata["source"]] for doc in retriever_docs]


if __name__ == '__main__':
    parser = DocParser("train_a.pdf")
    parser.parse_all_pages()
    bm25 = BM25(parser.data)
    recall_docs = bm25.get_bm_top_k("座椅加热", 3)
    print(recall_docs)
    

