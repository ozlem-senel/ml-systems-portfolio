"""
Create embeddings for knowledge base documents and build vector store.
Uses sklearn NearestNeighbors for efficient similarity search.
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


class EmbeddingManager:
    """Manage embeddings and vector search for RAG using sklearn."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize embedding model.
        
        Args:
            model_name: HuggingFace model for embeddings (384 dimensions)
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 embedding size
        self.nn_model = None
        self.embeddings = None
        self.documents = []
        
    def load_knowledge_base(self, kb_path: str) -> List[Dict]:
        """Load knowledge base documents from JSON file."""
        with open(kb_path, 'r') as f:
            documents = json.load(f)
        print(f"Loaded {len(documents)} documents from knowledge base")
        return documents
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for a list of texts."""
        print(f"Creating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def build_index(self, documents: List[Dict]):
        """Build vector index from knowledge base documents."""
        self.documents = documents
        
        # Combine title and content for better embeddings
        texts = [f"{doc['title']}. {doc['content']}" for doc in documents]
        
        # Create embeddings
        self.embeddings = self.create_embeddings(texts)
        
        # Build sklearn Nearest Neighbors model
        print("Building vector search index...")
        self.nn_model = NearestNeighbors(n_neighbors=min(5, len(documents)), metric='cosine')
        self.nn_model.fit(self.embeddings)
        
        print(f"Index built with {len(self.embeddings)} vectors")
        
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search for most relevant documents.
        
        Args:
            query: Search query text
            k: Number of results to return
            
        Returns:
            List of relevant documents with scores
        """
        if self.nn_model is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Create query embedding
        query_embedding = self.model.encode([query])
        
        # Search index
        distances, indices = self.nn_model.kneighbors(query_embedding, n_neighbors=k)
        
        # Return results with scores (convert cosine distance to similarity)
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            doc = self.documents[idx].copy()
            doc['score'] = float(1 - dist)  # Convert distance to similarity
            doc['rank'] = i + 1
            results.append(doc)
        
        return results
    
    def save(self, output_dir: str):
        """Save index and documents to disk."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save embeddings and model
        data = {
            'embeddings': self.embeddings,
            'documents': self.documents,
        }
        
        save_path = output_path / 'vector_store.pkl'
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Saved vector store to {save_path}")
    
    @classmethod
    def load(cls, model_name: str, index_dir: str):
        """Load index and documents from disk."""
        manager = cls(model_name=model_name)
        
        load_path = Path(index_dir) / 'vector_store.pkl'
        
        # Load data
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
        
        manager.embeddings = data['embeddings']
        manager.documents = data['documents']
        
        # Rebuild sklearn model
        manager.nn_model = NearestNeighbors(n_neighbors=min(5, len(manager.documents)), metric='cosine')
        manager.nn_model.fit(manager.embeddings)
        
        print(f"Loaded vector store with {len(manager.embeddings)} vectors")
        print(f"Loaded {len(manager.documents)} documents")
        
        return manager


def main():
    """Build embeddings and FAISS index."""
    # Initialize manager
    manager = EmbeddingManager()
    
    # Load knowledge base
    documents = manager.load_knowledge_base('data/knowledge_base/kb_documents.json')
    
    # Build index
    manager.build_index(documents)
    
    # Save index
    manager.save('vector_store')
    
    # Test search
    print("\n" + "="*50)
    print("Testing search functionality:")
    print("="*50)
    
    test_queries = [
        "My payment was declined",
        "App crashes when I open it",
        "How do I reset my password?",
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = manager.search(query, k=2)
        for result in results:
            print(f"  [{result['rank']}] {result['title']} (score: {result['score']:.3f})")
            print(f"      Category: {result['category']}")


if __name__ == '__main__':
    main()
