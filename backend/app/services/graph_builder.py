from app.services.document_loader import load_pdf
from app.utils.neo4j_client import add_triples_to_neo4j
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import tempfile
import json

def extract_triples_from_text(text):
    prompt = PromptTemplate.from_template("""
Extract entities and relationships from this paragraph and return in JSON:
Text: "{text}"
Respond in this JSON format:
{{
  "entities": [...],
  "relationships": [
    {{"from": "...", "to": "...", "type": "..."}}
  ]
}}
""")
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return result.content

async def build_graph_from_file(file):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # Step 1: Load
    documents = load_pdf(file_path)

    # Step 2: Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Step 3: Embed (optional, can remove if not needed)
    _ = FAISS.from_documents(chunks, OpenAIEmbeddings())

    # Step 4: Extract + Save to Neo4j
    for chunk in chunks:
        try:
            triples_json = extract_triples_from_text(chunk.page_content)
            data = json.loads(triples_json)
            add_triples_to_neo4j(data)
        except Exception as e:
            print(f"Skipping a chunk due to error: {e}")

    return "Graph successfully built and stored in Neo4j."
