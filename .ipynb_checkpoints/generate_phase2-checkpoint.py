from pathlib import Path

files = {

"app/data/rules/insurance_rules.txt": """
RULE_001
Policy number must be present.

RULE_002
Premium amount must be disclosed.

RULE_003
Customer signature is mandatory.

RULE_004
Nominee information should exist.

RULE_005
KYC identification details are required.
""",

"app/rag/embeddings.py": '''
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def get_embedding(text):
    return model.encode(text).tolist()
''',

"app/rag/vector_store.py": '''
import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="compliance_rules"
)
''',

"app/rag/ingest_rules.py": '''
from pathlib import Path

from app.rag.vector_store import collection
from app.rag.embeddings import get_embedding

RULE_FILE = "app/data/rules/insurance_rules.txt"

text = Path(RULE_FILE).read_text()

chunks = [
    chunk.strip()
    for chunk in text.split("\\n\\n")
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
''',

"app/agents/document_agent.py": '''
from app.services.document_parser import DocumentParser

class DocumentAgent:

    @staticmethod
    def process(path):
        return DocumentParser.parse(path)
''',

"app/agents/retrieval_agent.py": '''
from app.rag.vector_store import collection
from app.rag.embeddings import get_embedding

class RetrievalAgent:

    @staticmethod
    def retrieve(document_text):

        embedding = get_embedding(
            document_text[:2000]
        )

        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        return results["documents"][0]
''',

"app/api/validate.py": '''
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.file_service import FileService
from app.config.settings import settings

from app.agents.document_agent import DocumentAgent
from app.agents.retrieval_agent import RetrievalAgent

router = APIRouter()

@router.post("/validate")
async def validate(
    file: UploadFile = File(...)
):

    path = FileService.save_file(
        file,
        settings.UPLOAD_DIR
    )

    document_text = DocumentAgent.process(
        path
    )

    rules = RetrievalAgent.retrieve(
        document_text
    )

    return {
        "document": file.filename,
        "document_length": len(document_text),
        "matched_rules": rules
    }
'''
}

for filepath, content in files.items():

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("="*50)
print("PHASE 2 GENERATED")
print("="*50)
print()
print("Next:")
print("python -m app.rag.ingest_rules")
print("uvicorn app.main:app --reload")