import os
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from SERVICES.document_parser import parse_document
from SERVICES.embeddings import embed_texts
from SERVICES.vector_store import upsert_clauses
from AGENTS.extractor import extract_agent
from AGENTS.retriever import drift_agent
from AGENTS.risk_analyzer import risk_agent
from AGENTS.explainer import explain_agent

load_dotenv()

# LangGraph State 
state = {
    "doc_path": str,
    "metadata": dict,
    "blocks": [],
    "clauses": [],
    "events": [],
    "output": []
}


# Nodes

def parse_node(state):
    print("  -> Parsing document...")
    blocks = parse_document(state["doc_path"])
    return {"blocks": blocks, "metadata": state.get("metadata", {})}


def extract_node(state):
    print("  -> Extracting clauses...")
    clauses = extract_agent(state["blocks"], state["metadata"])
    return {"clauses": clauses, "blocks": state.get("blocks", [])}


def memory_node(state):
    texts = [c["text"] for c in state.get("clauses", [])]
    if texts:
        vectors = embed_texts(texts)
        upsert_clauses(state["clauses"], vectors)
    return {"clauses": state.get("clauses", []), "blocks": state.get("blocks", [])}


def drift_node(state):
    print("  -> Detecting changes...")
    clauses = state.get("clauses", [])
    events = []
    for clause in clauses:
        event = drift_agent(clause)
        if event:
            events.append(event)
    return {"events": events}


def risk_node(state):
    print("  -> Analyzing risks...")
    events = [risk_agent(e) for e in state["events"]]
    return {"events": events}


def explain_node(state):
    print("  -> Generating explanations...")
    explanations = [explain_agent(e) for e in state["events"]]
    return {"output": explanations}

# Graph Builder

def build_graph():
    g = StateGraph(dict)

    g.add_node("parse", parse_node)
    g.add_node("extract", extract_node)
    g.add_node("memory", memory_node)
    g.add_node("drift", drift_node)
    g.add_node("risk", risk_node)
    g.add_node("explain", explain_node)

    g.add_edge(START, "parse")
    g.add_edge("parse", "extract")
    g.add_edge("extract", "memory")
    g.add_edge("memory", "drift")
    g.add_edge("drift", "risk")
    g.add_edge("risk", "explain")
    g.add_edge("explain", END)

    return g.compile()


if __name__ == "__main__":
    graph = build_graph()

    documents = [
        {
            "doc_path": "data/contract_v1.pdf",
            "metadata": {
                "doc_id": "vendor_contract_001",
                "version": 1,
                "doc_type": "contract"
            }
        },
        {
            "doc_path": "data/internal_policy.pdf",
            "metadata": {
                "doc_id": "infosec_policy_abc",
                "version": 1,
                "doc_type": "policy"
            }
        },
        {
            "doc_path": "data/contract_v2.pdf",
            "metadata": {
                "doc_id": "vendor_contract_001",
                "version": 2,
                "doc_type": "contract"
            }
        }
    ]

    print("=" * 60)
    print("TRUSTLENS: AI-Powered Risk & Contract Intelligence")
    print("=" * 60)

    for doc in documents:
        try:
            print(f"\n[>] Processing: {doc['doc_path']}")
            result = graph.invoke(doc)

            if not result.get("output"):
                print("    [✓] No risks detected")
                continue

            print(f"    [!] Found {len(result['output'])} risk event(s)")
            for item in result["output"]:
                print("\n--- RISK EVENT ---")
                print(f"Change: {item.get('change_type', 'N/A')}")
                print(f"Risk: {item.get('risk', 'N/A')}")
                print(f"Explanation:\n{item.get('explanation', 'N/A')}")
        except Exception as e:
            print(f"[Error] {doc['doc_path']}: {str(e)}")
            import traceback
            traceback.print_exc()
