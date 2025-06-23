from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS"))
)

def add_triples_to_neo4j(data: dict):
    with driver.session() as session:
        for entity in data.get("entities", []):
            session.run("MERGE (e:Entity {name: $name})", name=entity)

        for rel in data.get("relationships", []):
            session.run("""
                MATCH (a:Entity {name: $from}), (b:Entity {name: $to})
                MERGE (a)-[:RELATION {type: $type}]->(b)
            """, parameters={
                "from": rel["from"],
                "to": rel["to"],
                "type": rel["type"]
            })

def close_driver():
    driver.close()
