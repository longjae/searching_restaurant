import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from google_maps import search_maps
from to_vector_store import get_retriever

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])
    
def search_restaurant(content):
    search_maps(content)
    print("RECOMMENDING=======================")
    template = """
    You are an expert in recommendation.
    Answer the question based only on the following context:

    {context}

    Question: {question}
    
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(temperature=0, api_key=OPENAI_API_KEY, model_name="gpt-4-0125-preview")

    retriever = get_retriever()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    user_prompt = """
        {content}의 평점이 가장 높고 영업중인 식당 3곳을 알려주는데, 만약 식당 이름이 영어로 나온다면 한글로 알려주면 좋겠어
        단, 평점이 5인 곳은 제외하고 알려줘
        알려줄 때 다음과 같이 알려줘
        
        검색한 맛집 결과는 다음과 같습니다.
        
        1. 식당이름-주소
        2. 식당이름-주소
        3. 식당이름-주소
        
        
    """
    
    result = chain.invoke(user_prompt)
    return result