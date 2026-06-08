try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    # Ephemeral mock memory collection for standalone local validation runs
    class MockCollection:
        def __init__(self):
            self.store = []
        def add(self, embeddings, metadatas, ids):
            for emb, meta, doc_id in zip(embeddings, metadatas, ids):
                self.store.append({"embedding": emb, "metadata": meta, "id": doc_id})
        def query(self, query_embeddings, n_results, where):
            matching_metadatas = []
            matching_distances = []
            user_id_filter = where.get("user_id") if where else None
            for item in self.store:
                if not user_id_filter or item["metadata"].get("user_id") == user_id_filter:
                    matching_metadatas.append(item["metadata"])
                    matching_distances.append(0.0) # Mock similarity score
            return {
                "metadatas": [matching_metadatas[:n_results]],
                "distances": [matching_distances[:n_results]]
            }

    class MockClient:
        def get_or_create_collection(self, name, metadata=None):
            return MockCollection()

    class MockChromaDB:
        def PersistentClient(self, path, settings=None):
            return MockClient()
        class Settings:
            def __init__(self, **kwargs): pass

    import sys
    sys.modules['chromadb'] = MockChromaDB()
    sys.modules['chromadb.config'] = MockChromaDB()
    import chromadb
    from chromadb.config import Settings

from typing import List, Dict, Any, Optional
from shared.config import settings


class CognitiveMemoryStore:
    def __init__(self):
        # Initialize persistent or ephemeral ChromaDB client based on configuration settings
        if settings.VECTOR_DB_PROVIDER == "chroma":
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=Settings(anonymized_telemetry=False)
            )
            # Create or get standard user semantic history collection
            self.collection = self.client.get_or_create_collection(
                name="user_semantic_memory",
                metadata={"hnsw:space": "cosine"} # Use cosine similarity for emotion vectors
            )
        else:
            self.client = None
            self.collection = None

    def store_semantic_state(self, user_id: str, embedding: List[float], metadata: Dict[str, Any], doc_id: str) -> bool:
        """Stores a computed cognitive/emotional vector mapping with associated state metadata."""
        if not self.collection:
            return False

        # Add user reference to metadata
        metadata["user_id"] = user_id
        
        self.collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return True

    def query_semantic_history(self, user_id: str, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the vector database for historically similar cognitive patterns for a specific user."""
        if not self.collection:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"user_id": user_id} # Strictly isolate queries to the target user
        )
        
        # Flatten and format returned documents and metadata
        formatted_results = []
        if results and "metadatas" in results and results["metadatas"]:
            for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
                formatted_results.append({
                    "metadata": meta,
                    "distance_score": float(dist)
                })
                
        return formatted_results
