"""Lightweight TF-IDF retrieval used by the RAG pipeline."""

import json
import pickle
from pathlib import Path
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingManager:
    """Build, save, load, and query a small local vector store."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.embeddings = None
        self.documents: List[Dict] = []

    def build_index(self, documents: List[Dict]) -> None:
        self.documents = documents
        texts = [f"{doc['title']}. {doc['content']}" for doc in documents]
        self.embeddings = self.vectorizer.fit_transform(texts)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        if self.embeddings is None:
            raise ValueError("Index is not built")

        scores = cosine_similarity(self.vectorizer.transform([query]), self.embeddings)[0]
        indices = scores.argsort()[::-1][: min(k, len(self.documents))]
        results = []
        for rank, index in enumerate(indices, start=1):
            document = self.documents[index].copy()
            document.update(score=float(scores[index]), rank=rank)
            results.append(document)
        return results

    def save(self, index_dir: str | Path) -> None:
        path = Path(index_dir)
        path.mkdir(parents=True, exist_ok=True)
        with (path / "vector_store.pkl").open("wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_or_build(cls, index_dir: str | Path, knowledge_base_path: str | Path):
        """Load a compatible index, or create it automatically from the JSON KB."""
        index_path = Path(index_dir) / "vector_store.pkl"
        if index_path.exists():
            try:
                with index_path.open("rb") as file:
                    manager = pickle.load(file)
                if isinstance(manager, cls):
                    return manager
            except (AttributeError, ModuleNotFoundError, pickle.UnpicklingError, EOFError):
                pass

        with Path(knowledge_base_path).open(encoding="utf-8") as file:
            documents = json.load(file)
        manager = cls()
        manager.build_index(documents)
        manager.save(index_dir)
        return manager


def main() -> None:
    project_dir = Path(__file__).resolve().parent.parent
    manager = EmbeddingManager.load_or_build(
        project_dir / "vector_store",
        project_dir / "data/knowledge_base/kb_documents.json",
    )
    for result in manager.search("My payment was declined", k=2):
        print(f"{result['title']} ({result['score']:.3f})")


if __name__ == "__main__":
    main()
