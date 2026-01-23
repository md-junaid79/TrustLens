import os
from langchain_groq import ChatGroq
from UTILS.prompts import RISK_ANALYSIS_PROMPT
from dotenv import load_dotenv
load_dotenv()

try:
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"), timeout=10)
except Exception as e:
    print(f"[-] LLM initialization failed: {str(e)}")
    llm = None

def risk_agent(event):
    if not llm:
        event["risk"] = "Unknown"
        return event
    
    try:
        base_signal = "Low"

        if event["type"] == "modified":
            if "shall" in event["new"]["text"].lower() and "may" in event["old"]["text"].lower():
                base_signal = "Medium"

        prompt = f"""
Base heuristic risk: {base_signal}
Old clause: {event.get("old", {}).get("text","")}
New clause: {event.get("new", {}).get("text","")}
"""

        label = llm.invoke(RISK_ANALYSIS_PROMPT + prompt).content.strip()
        event["risk"] = label
        return event
    except Exception as e:
        print(f"[-] Risk analysis error: {str(e)}")
        event["risk"] = "Error"
        return event
