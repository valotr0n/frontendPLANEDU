from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="llama3.1:8b-instruct-q5_K_S")
    return embeddings