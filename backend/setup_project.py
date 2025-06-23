import os

folders = [
    "app",
    "app/routes",
    "app/services",
    "app/utils",
    "tests"
]

files = {
    "app/main.py": '''from fastapi import FastAPI
from app.routes import graph

app = FastAPI()
app.include_router(graph.router, prefix="/api")
''',

    "app/routes/graph.py": '''from fastapi import APIRouter, UploadFile
from app.services.graph_builder import build_graph_from_file

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile):
    result = await build_graph_from_file(file)
    return {"status": "success", "summary": result}
''',

    "app/services/document_loader.py": '''# Document loader using LangChain
from langchain.document_loaders import PyMuPDFLoader

def load_pdf(path):
    loader = PyMuPDFLoader(path)
    return loader.load()
''',

    "app/services/graph_builder.py": '''# Graph builder from documents
async def build_graph_from_file(file):
    # Placeholder logic for processing and graph generation
    return "Graph successfully built from uploaded file."
''',

    "app/utils/neo4j_client.py": '''from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS"))
)

def add_node(tx, label, props):
    tx.run(f"CREATE (n:{label} $props)", props=props)
''',

    "requirements.txt": '''fastapi
uvicorn
neo4j
langchain
PyMuPDF
openai
python-dotenv
unstructured
pymupdf
''',

    ".env": '''NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_password
OPENAI_API_KEY=your_openai_key
''',

    "README.md": '''# Neo4j LLM Knowledge Graph Builder

A FastAPI + LangChain + Neo4j-based backend that extracts knowledge graphs from unstructured files.
'''
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with content
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project scaffold created successfully!")
