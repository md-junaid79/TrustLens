import os
from langchain_groq import ChatGroq
from UTILS.prompts import EXPLANATION_PROMPT

try:
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"), timeout=10)
except Exception as e:
    print(f"[-] LLM initialization failed: {str(e)}")
    llm = None

def explain_agent(event):
    if not llm:
        return {
            "change_type": event["type"],
            "risk": event["risk"],
            "explanation": "LLM unavailable",
            "evidence": {
                "old_version": event.get("old", {}).get("version"),
                "new_version": event.get("new", {}).get("version")
            }
        }
    
    try:
        explanation = llm.invoke(
            EXPLANATION_PROMPT +
            f"\nOLD:\n{event.get('old',{}).get('text','')}\nNEW:\n{event.get('new',{}).get('text','')}",
            timeout=10
        ).content

        return {
            "change_type": event["type"],
            "risk": event["risk"],
            "explanation": explanation,
            "evidence": {
                "old_version": event.get("old", {}).get("version"),
                "new_version": event.get("new", {}).get("version")
            }
        }
    except Exception as e:
        print(f"⚠️  Explanation generation error: {str(e)}")
        return {
            "change_type": event["type"],
            "risk": event["risk"],
            "explanation": f"Error: {str(e)}",
            "evidence": {
                "old_version": event.get("old", {}).get("version"),
                "new_version": event.get("new", {}).get("version")
            }
        }
