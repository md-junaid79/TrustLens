from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, VectorParams, Distance
import uuid
import os

client = None
COLLECTION = "legal_docs"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 dimension

try:
    client = QdrantClient(url="http://localhost:6333", timeout=5.0)
    # Test connection
    client.get_collections()
    print("[OK] Qdrant connected")
    
    # Create collection if it doesn't exist
    try:
        client.get_collection(COLLECTION)
        print(f"[OK] Collection '{COLLECTION}' exists")
    except Exception:
        print(f"[*] Creating collection '{COLLECTION}'...")
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
        print(f"[OK] Collection '{COLLECTION}' created")
        
except Exception as e:
    print(f"[-] Qdrant unavailable: {str(e)}. Running in memory mode.")
    client = None

def upsert_clauses(clauses, vectors):
    if not client:
        print("[-] Vector store disabled - Qdrant unavailable")
        return
    
    try:
        points = []
        for c, v in zip(clauses, vectors):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=v,
                    payload=c
                )
            )
        client.upsert(collection_name=COLLECTION, points=points)
        print(f"[OK] Upserted {len(points)} clauses")
    except Exception as e:
        print(f"[-] Upsert error: {str(e)}")

def search_previous_versions(vector, doc_id, version):
    if not client:
        return []
    
    try:
        flt = Filter(
            must=[
                FieldCondition(key="doc_id", match=MatchValue(value=doc_id)),
                FieldCondition(key="version", range={"lt": version})
            ]
        )

        return client.search(
            collection_name=COLLECTION,
            query_vector=vector,
            query_filter=flt,
            limit=1,
            timeout=5
        )
    except Exception as e:
        print(f"[-] Search error: {str(e)}")
        return []
