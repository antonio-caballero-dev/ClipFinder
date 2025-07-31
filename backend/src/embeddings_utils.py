from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

from src.config import SENTENCE_TRANSFORMERS_DIR

def load_embedding_model(model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    """
    Carga el modelo de embeddings de SentenceTransformers.
    """
    print(f"Cargando modelo de embeddings: {model_name}...")
    model = SentenceTransformer(model_name, cache_folder=SENTENCE_TRANSFORMERS_DIR)
    return model

def embed_texts(model, texts: List[str]) -> np.ndarray:
    """
    Genera embeddings para una lista de textos.
    """
    print(f"Generando embeddings para {len(texts)} textos...")
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

def save_embeddings(embeddings: np.ndarray, filepath: str):
    """
    Guarda los embeddings en un archivo numpy.
    """
    np.save(filepath, embeddings)

def load_embeddings(filepath: str) -> np.ndarray:
    """
    Carga embeddings desde un archivo numpy.
    """
    return np.load(filepath)

def search_top_k(query_embedding: np.ndarray, embeddings: np.ndarray, top_k: int = 5):
    """
    Busca los top_k embeddings más similares al embedding de consulta usando similitud coseno.
    Utiliza sklearn.metrics.pairwise.cosine_similarity para calcular la similitud.
    """
    similarities = cosine_similarity(embeddings, query_embedding.reshape(1, -1)).flatten()
    top_indices = np.argpartition(-similarities, top_k)[:top_k]
    top_indices = top_indices[np.argsort(-similarities[top_indices])]
    return [(i, similarities[i]) for i in top_indices]

