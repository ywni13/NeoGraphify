def parse_file_to_triples(text: str) -> dict:
    entities = set()
    relationships = []

    for line in text.splitlines():
        if "->" in line:
            from_ent, to_ent = map(str.strip, line.split("->"))
            entities.update([from_ent, to_ent])
            relationships.append({
                "from": from_ent,
                "to": to_ent,
                "type": "related_to"
            })

    return {
        "entities": list(entities),
        "relationships": relationships
    }
