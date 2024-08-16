from sentence_transformers import SentenceTransformer
import torch
import logging

EMBEDDING_MODEL_ID = "thenlper/gte-small"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_ID, device=device)

def get_embedding(text: str) -> list[float]:
    if not text.strip():
        logging.warn("Empty text provided for embedding")
        return []

    embedding = embedding_model.encode(text, device=device)
    return embedding.tolist()
