def extract_agent(parsed_blocks, metadata):
    clauses = []

    for i, block in enumerate(parsed_blocks):
        clauses.append({
            "clause_id": f"{metadata['doc_id']}_{metadata['version']}_{i}",
            "text": block["text"],
            "section_type": block["type"],
            "doc_id": metadata["doc_id"],
            "version": metadata["version"],
            "doc_type": metadata["doc_type"]
        })

    return clauses
