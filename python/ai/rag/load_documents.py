from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    document_loader = PyPDFLoader("data/zombie.pdf")
    return document_loader.load()
load_documents()