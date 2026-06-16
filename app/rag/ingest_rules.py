
from pathlib import Path

from app.rag.vector_store import collection
from app.rag.embeddings import get_embedding

RULE_FILE = "app/data/rules/insurance_rules.txt"

text = Path(RULE_FILE).read_text()

chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

for idx, chunk in enumerate(chunks):

    try:
        collection.add(
            ids=[f"rule_{idx}"],
            documents=[chunk],
            embeddings=[get_embedding(chunk)]
        )
    except:
        pass

print("Rules indexed successfully")
