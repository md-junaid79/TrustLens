from SERVICES.embeddings import embed_texts
from SERVICES.vector_store import search_previous_versions

SIM_HIGH = 0.88
SIM_LOW = 0.65

def drift_agent(clause):
    try:
        vec = embed_texts([clause["text"]])[0]
        hits = search_previous_versions(vec, clause["doc_id"], clause["version"])

        if not hits:
            return {"type": "new", "new": clause}

        hit = hits[0]
        score = hit.score
        old = hit.payload

        if score >= SIM_HIGH:
            return None
        if score >= SIM_LOW:
            return {"type": "modified", "old": old, "new": clause}

        return {"type": "new", "new": clause}
    except Exception as e:
        print(f"[-] Drift detection error: {str(e)}")
        return {"type": "new", "new": clause}
