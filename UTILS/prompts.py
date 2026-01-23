CLAUSE_EXTRACTION_PROMPT = """Extract all contractual clauses from the following document text.
Return a JSON list where each item has:
- clause_number: sequential number
- clause_text: the full clause text
- clause_type: category (e.g., payment, termination, liability, warranty, general)

Document Text:
{document_text}
Return ONLY valid JSON, no other text."""

RISK_ANALYSIS_PROMPT = """Analyze the following clause changes for risk:

Original Clause: {original_clause}
Modified Clause: {modified_clause}
Change Type: {change_type}

Evaluate:
1. Does this increase legal/financial risk?
2. Are protective terms removed or weakened?
3. Is ambiguity introduced?

Return JSON:
{{
  "risk_level": "Low|Medium|High",
  "risk_reason": "brief explanation",
  "concern_areas": ["area1", "area2"]
}}
Return ONLY valid JSON."""

POLICY_CHECK_PROMPT = """Check if this clause contradicts the policy:

Clause: {clause_text}
Policy Document: {policy_text}

Return JSON:
{{
  "contradicts": true/false,
  "explanation": "why it contradicts or aligns"
}}
Return ONLY valid JSON."""

EXPLANATION_PROMPT = """Generate a clear, professional summary of contract changes and risks.

Drift Results: {drift_results}
Risk Signals: {risk_signals}

Create a report with:
1. Executive Summary
2. Key Changes Detected
3. Risk Assessment
4. Evidence References
Use clear language. SIMPLE ENGLISH. Focus on facts and evidence."""