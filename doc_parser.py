from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import config


class DocParser(object):
    """
    调用 ocr接口，识别内容，切分文件。此处以一个 pdf文件为例。
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse_and_split(self, chunk_size=256, chunk_overlap=100) -> list[Document]:
        docs = PyPDFLoader(self.file_path).load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                       chunk_overlap=chunk_overlap, 
                                                       add_start_index=True)
        return text_splitter.split_documents(docs)
        
        
if __name__ == '__main__':
    file_path = config.PATH_FILE_KN
    docs = DocParser(file_path).parse_and_split()
    print(docs)

