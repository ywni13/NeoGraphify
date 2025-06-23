from langchain.document_loaders import PyMuPDFLoader

def load_pdf(path):
    loader = PyMuPDFLoader(path)
    return loader.load()
