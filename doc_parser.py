import os.path

import pdfplumber

from config import cfg

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from loguru import logger
from PyPDF2 import PdfReader


class DocParser(object):

    def __init__(self, file_name: str, file_dir_path: str = cfg.PATH_DATA_DIR):
        self.file_dir_path = file_dir_path
        self.file_path = os.path.join(self.file_dir_path, file_name)  # 指定处理文件夹中的某个文件
        self.data = []

    def parse_and_split(self, chunk_size=256, chunk_overlap=100) -> list[Document]:
        docs = PyPDFLoader(self.file_path).load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                       chunk_overlap=chunk_overlap, 
                                                       add_start_index=True)
        return text_splitter.split_documents(docs)

    @classmethod
    def get_header(cls, page):
        """获取单个page页的标题，可作为该页内容的标签内容"""
        try:
            lines = page.extract_words()
        except Exception as e:
            logger.error(fr'get_header过程异常，原因:{e}')
            return None
        if len(lines) > 0:
            for line in lines:
                if("目录" in line["text"] or ".........." in line["text"]):
                    return None
                if line["top"] < 20 and line["top"] > 17:
                    return line["text"]
            return lines[0]["text"]
        return None

    def data_filter(self, line, max_seq_len=1024):
        """过滤长度过短的句子，根据max_seq划分文档块，并对文档块文本ETL"""

        sz = len(line)
        if sz < 6:  # 当该行内容过短时，过滤掉
            return

        if sz > max_seq_len:

            if "■" in line:
                sentences = line.split("■")
            elif "•" in line:
                sentences = line.split("•")
            elif "\t" in line:
                sentences = line.split("\t")
            else:
                sentences = line.split("。")

            for sentence in sentences:
                sentence = sentence.replace("\n", "")

                if len(sentence) < max_seq_len & len(sentence) > 5:
                    sentence = sentence.replace(",", "").replace("\n","").replace("\t","")
                    self.data.append(sentence)

        else:
            line = line.replace("\n", "").replace(",", "").replace("\t", "")
            if line not in self.data:
                self.data.append(line)

    def parse_block(self, max_seq = 1024):
        """按照每页中块提取内容,并和一级标题进行组合,配合Document 可进行意图识别"""
        with pdfplumber.open(self.file_path) as pdf:

            for i, p in enumerate(pdf.pages):
                header = DocParser.get_header(p)

                if header is None:
                    continue

                texts = p.extract_words(use_text_flow=True, extra_attrs = ["size"])[::]

                sequence = ""
                lastsize = 0

                for idx, line in enumerate(texts):
                    if idx < 1:
                        continue
                    if idx == 1:
                        if line["text"].isdigit():
                            continue
                    cursize = line["size"]
                    text = line["text"]
                    if text == "□" or text == "•":
                        continue
                    elif text=="警告！" or text == "注意！" or text == "说明！":
                        if len(sequence) > 0:
                            self.data_filter(sequence, max_seq_len=max_seq)
                        sequence = ""
                    elif format(lastsize,".5f") == format(cursize,".5f"):
                        if len(sequence) > 0:
                            sequence = sequence + text
                        else:
                            sequence = text
                    else:
                        lastsize = cursize
                        if 15 > len(sequence) > 0:
                            sequence = sequence + text
                        else:
                            if len(sequence) > 0:
                                self.data_filter(sequence, max_seq_len=max_seq)
                            sequence = text
                if len(sequence) > 0:
                    self.data_filter(sequence, max_seq_len=max_seq)

    def sliding_windows(self, lines: list[str], chunk_size=512):
        """
        合并句子列表，overlap为1个句子。
        lines: 待合并的句子列表。
        chunk_size: 每个合并后的句子的长度最大值。
        """
        cur_size = 0
        start_index = 0
        for i in range(0, len(lines)):
            cur_size += len(lines[i])
            if cur_size >= chunk_size:
                chunk_lines = "。".join(lines[start_index:i+1]) + "。"
                if chunk_lines not in self.data:
                    self.data.append(chunk_lines)

                start_index = i
                cur_size = 0
        if start_index < len(lines)-1:
            chunk_lines = "。".join(lines[start_index:]) + "。"
            if chunk_lines not in self.data:
                self.data.append(chunk_lines)

    def parse_all_pages(self, chunk_size=512, min_seq_len=6):
        """
        获取所有文档页的内容，以句号为分隔符切分成一个数组，滑窗法合并数组并以一个句子为overlap
        chunk_size:
        min_seq_len: 过滤小于该长度的句子。
        """
        all_content = ""
        for idx, page in enumerate(PdfReader(self.file_path).pages):
            page_content = ""
            text = page.extract_text()
            _words = text.split("\n")
            for word in _words:
                text = word.strip().strip("\n")
                if "...................." in text or "目录" in text:
                    continue
                if len(text) < 1:
                    continue
                if text.isdigit():
                    continue
                page_content += text

            if len(page_content) < min_seq_len:
                continue
            all_content += page_content
        sentences = all_content.split("。")
        self.sliding_windows(sentences, chunk_size=chunk_size)

        
if __name__ == '__main__':
    file_name = "train_a.pdf"
    parser = DocParser(file_name)


