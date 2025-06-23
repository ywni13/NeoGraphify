from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import graph

app = FastAPI(
    title="Neo4j LLM Knowledge Graph Builder",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph.router, prefix="/api")
