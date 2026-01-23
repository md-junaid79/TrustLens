"""Setup Qdrant collections for TrustLens"""

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def setup_qdrant():
    try:
        client = QdrantClient(url="http://localhost:6333", timeout=5.0)
        
        # Check existing collections
        collections = client.get_collections()
        existing = [c.name for c in collections.collections]
        print(f"[*] Existing collections: {existing if existing else 'None'}")
        
        # Create legal_docs collection
        if "legal_docs" not in existing:
            print("[*] Creating 'legal_docs' collection...")
            client.create_collection(
                collection_name="legal_docs",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("[OK] Collection 'legal_docs' created successfully")
        else:
            print("[OK] Collection 'legal_docs' already exists")
            
        # Verify
        collections = client.get_collections()
        final = [c.name for c in collections.collections]
        print(f"[+] Final collections: {final}")
        
    except Exception as e:
        print(f"[ERROR] Failed to setup Qdrant: {e}")
        print("[INFO] Make sure Qdrant is running at http://localhost:6333")

if __name__ == "__main__":
    setup_qdrant()
