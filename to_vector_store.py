import os

from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_retriever():
    loader = TextLoader("data.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    db = FAISS.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5})
    
    return retriever