import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

load_dotenv()

# Keep the ChromaDB directory at the project root so existing local data can be reused.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(PROJECT_ROOT, "school_db"))

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="school_faqs",
    embedding_function=embedding_function,
)

def search_school_faq(question: str, institution_id: str, n_results: int = 3):
    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, count),
        where={"institution_id": str(institution_id)},
        include=["documents", "distances", "metadatas"],
    )

    documents = (results.get("documents") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    relevant_documents = []
    for document, distance in zip(documents, distances):
        if document and distance is not None and distance <= 0.60:
            relevant_documents.append(document)
    return relevant_documents
