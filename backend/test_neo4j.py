# test_neo4j.py
import inspect
import app.utils.neo4j_client as neo4j_client

print([name for name, obj in inspect.getmembers(neo4j_client) if inspect.isfunction(obj)])

from app.utils.neo4j_client import add_triples_to_neo4j


sample_data = {
    "entities": ["Neo4j", "LLMs", "LangChain"],
    "relationships": [
        {"from": "Neo4j", "to": "LLMs", "type": "integrates with"},
        {"from": "Neo4j", "to": "LangChain", "type": "uses"}
    ]
}

add_triples_to_neo4j(sample_data)
print("Data added to Neo4j!")
