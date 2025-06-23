from fastapi import APIRouter, UploadFile, File
import os
import uuid
from app.services.extractor import extract_knowledge_from_pdf
from app.utils.neo4j_client import add_triples_to_neo4j

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"temp_files/{uuid.uuid4()}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    triples = extract_knowledge_from_pdf(file_location)
    add_triples_to_neo4j(triples)

    return {"message": "Knowledge graph created"}
