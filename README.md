# TrustLens

A multi-agent, retrieval-based AI system powered by **Qdrant** that detects clause drift, hidden risk escalation, and policy contradictions across contract versions. TrustLens uses long-term semantic memory and evidence-grounded reasoning to surface what changed, why it matters, and where the evidence comes from.

---

## 🎯 Overview

TrustLens leverages a sophisticated multi-agent architecture built with **LangGraph** to analyze legal documents comprehensively:

- **Clause Drift Detection**: Identifies modifications in contract clauses across versions
- **Risk Escalation Analysis**: Uncovers hidden changes that may increase liability or obligations
- **Policy Contradiction Detection**: Surfaces conflicting terms within and across documents
- **Semantic Memory**: Uses Qdrant vector database for efficient clause retrieval and similarity matching
- **Evidence-Grounded Explanations**: Provides clear explanations of detected changes with supporting evidence

---
## 📊 Project Structure

```
trustlens/
├── main.py                      # LangGraph pipeline orchestrator
├── notebook.ipynb               # Interactive analysis notebook
├── setup_qdrant.py              # Qdrant initialization script
├── requirements.txt             # Python dependencies
│
├── AGENTS/                      # Specialized analysis agents
│   ├── __init__.py
│   ├── extractor.py             # Clause extraction logic
│   ├── retriever.py             # Drift detection & retrieval
│   ├── risk_analyzer.py         # Risk assessment with LLM
│   └── explainer.py             # Explanation generation
│
├── SERVICES/                    # Core services
│   ├── __init__.py
│   ├── document_parser.py       # PDF/text parsing
│   ├── embeddings.py            # Vector generation
│   └── vector_store.py          # Qdrant integration
│
├── UTILS/                       # Utilities
│   ├── __init__.py
│   └── prompts.py               # LLM prompt templates
│
└── data/                        # Sample documents
    ├── contract_v1.pdf
    └── contract_v2.pdf
```
## 🏗️ Architecture

### Multi-Agent Pipeline

TrustLens implements a LangGraph-based state machine with six specialized agents:

```
Document → Parse → Extract → Embed & Store → Drift Detection → Risk Analysis → Explanation
   (PDF)     (Text)  (Clauses)  (Qdrant)       (Compare)        (Analyze)      (LLM)
```

### Core Components

#### **1. Document Parser** (`SERVICES/document_parser.py`)
- Parses PDF and text documents into structured blocks
- Preserves document structure and metadata
- Supports multiple document formats

#### **2. Embeddings Service** (`SERVICES/embeddings.py`)
- Uses `sentence-transformers` (all-MiniLM-L6-v2, 384-dim vectors)
- Converts clause text to semantic vectors
- Enables similarity-based clause matching

#### **3. Vector Store** (`SERVICES/vector_store.py`)
- Manages Qdrant collections for persistent storage
- Stores clause vectors with full metadata payloads
- Supports semantic search and filtering
- **Collection**: `legal_docs` (384-dim COSINE distance)

#### **4. Extraction Agent** (`AGENTS/extractor.py`)
- Extracts structured clauses from parsed document blocks
- Assigns unique clause IDs with version tracking
- Captures clause metadata (section type, document type, version)

#### **5. Drift Detection Agent** (`AGENTS/retriever.py`)
- Retrieves similar clauses from vector store
- Compares old vs. new clause versions
- Detects modifications, additions, and deletions
- Generates drift events with change metadata

#### **6. Risk Analysis Agent** (`AGENTS/risk_analyzer.py`)
- Uses LLM (Groq GPT-4 compatible) for semantic risk assessment
- Applies heuristic rules (e.g., "shall" vs. "may" changes)
- Labels risks as Low/Medium/High
- Provides risk explanations

#### **7. Explanation Agent** (`AGENTS/explainer.py`)
- Generates human-readable explanations
- Contextualizes risks with evidence references
- Creates actionable insights for legal teams

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Qdrant Server** running at `http://localhost:6333`
- **Groq API Key** for LLM access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/trustlens.git
   cd trustlens
   ```

2. **Set up Python environment**
   ```bash
   conda create -n trustlens python=3.11
   conda activate trustlens
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Groq API key
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   ```

5. **Start Qdrant Server**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:latest
   ```

6. **Initialize Qdrant collections**
   ```bash
   python setup_qdrant.py
   ```

---

## 📦 Dependencies

```
langgraph==0.6.7              # Multi-agent orchestration
langchain-groq==0.2.5         # LLM integration
unstructured==0.15.0          # Document parsing
sentence-transformers==3.4.1  # Semantic embeddings
qdrant-client==1.11.0         # Vector database client
python-dotenv==1.0.0          # Environment configuration
```

---

## 💻 Usage

### Basic Example

```python
from main import build_graph

# Build the analysis pipeline
graph = build_graph()

# Prepare documents
documents = [
    {
        "doc_path": "data/contract_v1.pdf",
        "metadata": {
            "doc_id": "vendor_contract_001",
            "version": "1.0",
            "doc_type": "vendor_agreement",
            "date": "2024-01-15"
        }
    },
    {
        "doc_path": "data/contract_v2.pdf",
        "metadata": {
            "doc_id": "vendor_contract_001",
            "version": "2.0",
            "doc_type": "vendor_agreement",
            "date": "2024-12-01"
        }
    }
]

# Run analysis
for doc in documents:
    result = graph.invoke(doc)
    
    # Process results
    for explanation in result["output"]:
        print(f"Finding: {explanation['text']}")
        print(f"Risk Level: {explanation['risk']}")
        print(f"Evidence: {explanation['evidence']}")
```

### Running the Pipeline

```bash
# Execute full analysis
python main.py

# Run Jupyter notebook (interactive analysis)
jupyter notebook notebook.ipynb
```




---

## 🔄 Data Flow

### 1. **Parse Node**
- Input: Document path
- Process: Extract text blocks from PDF/document
- Output: Structured text blocks with metadata

### 2. **Extract Node**
- Input: Text blocks
- Process: Segment into clauses, assign IDs
- Output: Structured clauses with metadata

### 3. **Memory Node**
- Input: Clauses
- Process: Generate embeddings, store in Qdrant
- Output: Persisted vectors in semantic space

### 4. **Drift Node**
- Input: Current clauses
- Process: Retrieve similar versions from Qdrant, compare
- Output: Drift events (modifications, additions, deletions)

### 5. **Risk Node**
- Input: Drift events
- Process: LLM-based risk analysis
- Output: Enriched events with risk labels

### 6. **Explain Node**
- Input: Risk-analyzed events
- Process: Generate human-readable explanations
- Output: Final insights and recommendations

---

## 🔧 Configuration

### Environment Variables

```bash
# .env file
GROQ_API_KEY=your_api_key_here
QDRANT_URL=http://localhost:6333
QDRANT_TIMEOUT=5.0
VECTOR_DIMENSION=384  # all-MiniLM-L6-v2
COLLECTION_NAME=legal_docs
```

### Qdrant Collection Schema

```
Collection: legal_docs
- Vector Size: 384 dimensions
- Distance Metric: COSINE
- Payload Fields:
  - clause_id (string): Unique clause identifier
  - text (string): Clause content
  - section_type (string): Document section
  - doc_id (string): Parent document ID
  - version (string): Document version
  - doc_type (string): Contract type
```

---

## 📈 Example Output

```json
{
  "clause_id": "vendor_contract_001_2.0_5",
  "type": "modified",
  "old": {
    "text": "Vendor may terminate this agreement with 30 days notice.",
    "version": "1.0"
  },
  "new": {
    "text": "Vendor shall terminate this agreement with 90 days notice.",
    "version": "2.0"
  },
  "risk": "High",
  "explanation": "Term extended from 30 to 90 days. Changed 'may' to 'shall' (mandatory obligation). Increases buyer's risk exposure by 2 months of service dependency.",
  "evidence": [
    "Modified termination clause",
    "Changed modal verb from 'may' (optional) to 'shall' (mandatory)"
  ]
}
```

---

## 🎓 Use Cases

1. **Contract Review**: Automated detection of changes between contract versions
2. **Risk Assessment**: Identify high-risk modifications before signing
3. **Compliance Monitoring**: Track policy changes across documents
4. **Legal Intelligence**: Build semantic search over contract databases
5. **Document Auditing**: Detect contradictions and inconsistencies

---

## 🔍 Advanced Features

### Semantic Search
Query the vector store for similar clauses:
```python
from SERVICES.vector_store import client

# Find similar clauses
search_results = client.search(
    collection_name="legal_docs",
    query_vector=query_embedding,
    limit=10
)
```

### Filtered Retrieval
Retrieve clauses by metadata:
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = client.search(
    collection_name="legal_docs",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="doc_type", match=MatchValue(value="vendor_agreement")),
            FieldCondition(key="version", match=MatchValue(value="2.0"))
        ]
    )
)
```

---

## 🐛 Troubleshooting

### Qdrant Connection Error
```
[-] Qdrant unavailable: Connection refused. Running in memory mode.
```
**Solution**: Ensure Qdrant is running:
```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

### LLM Initialization Failed
```
[-] LLM initialization failed: API key not found
```
**Solution**: Set GROQ_API_KEY in .env file

### Vector Dimension Mismatch
Ensure all embeddings use the same model (all-MiniLM-L6-v2, 384-dim)

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

## 🔗 Related Technologies

- **[LangGraph](https://langchain-ai.github.io/langgraph/)**: Multi-agent orchestration
- **[Qdrant](https://qdrant.tech/)**: Vector database
- **[Sentence Transformers](https://www.sbert.net/)**: Semantic embeddings
- **[Groq](https://groq.com/)**: Fast LLM inference
- **[LangChain](https://www.langchain.com/)**: LLM framework

---

**Built with ❤️ for legal AI professionals**
