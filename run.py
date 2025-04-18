from pydoc import doc
import config

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import SystemMessage, HumanMessage

from doc_parser import DocParser
from faiss_retriever import FaissRetriever
from rerank_model import Reranker


def get_kn_by_query(question: str) -> str:
    kn_path = config.PATH_FILE_KN
    model_path = config.PATH_BGE_M3
    rerank_model_path = config.PATH_BGE_RERANKER

    kn_data = DocParser(file_path=kn_path).parse_and_split()
    retriever = FaissRetriever(model_path=model_path, kn_data=kn_data)
    reRanker = Reranker(rerank_model_path)

    retriever_result = retriever.get_top_k(question)
    rank_result = reRanker.predict(question, retriever_result)
    print('检索结果：', [res.page_content for res in retriever_result])
    print('rerank结果：', rank_result)
    return "\n\n".join(rank_result)



def question_answer(query):
    llm = ChatZhipuAI(
        model='glm-4-flash',
        temperature=0.5,
        api_key = config.ZHIPU_API_KEY
    )
    doc_str = get_kn_by_query(query)

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
    llm_answer = question_answer(user_question)
    print('='*10, '问答结果', '='*10)
    print('用户提问:', user_question)
    print('模型回答:', llm_answer)









