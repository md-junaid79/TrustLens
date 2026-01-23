from sentence_transformers import SentenceTransformer
import time

print("[*] Loading embedding model (one-time cost)...")
start = time.time()
text_model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"[OK] Model loaded in {time.time() - start:.1f}s")

def embed_texts(texts):
    if not texts:
        return []
    start = time.time()
    result = text_model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()
    print(f"[OK] Embedded {len(texts)} texts in {time.time() - start:.2f}s")
    return result
