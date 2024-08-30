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

def search_restaurant(content):
    search_maps(content)
    print("RECOMMENDING=======================")
    template = """Answer the question based only on the following context:

    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(temperature=0, api_key=OPENAI_API_KEY, model_name="gpt-4-0125-preview")

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    retriever = get_retriever()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    prompt = """
        {content}의 평점이 가장 높고 영업중인 식당 3곳을 알려줘
        단, 평점이 5인 곳은 제외하고 알려줘
        알려줄 때 다음과 같이 알려줘
        
        1. 식당이름-주소
        2. 식당이름-주소
        3. 식당이름-주소
    """
    
    result = chain.invoke(prompt)
    return result