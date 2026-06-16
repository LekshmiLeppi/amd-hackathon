
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
