from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..utils.helpers import load_config, safe_api_call
import json

# Load config
config = load_config()
api_key = config["openai_api_key"]
temperature = config.get("model_temperature", 0.3)

# Updated state model to support nested dictionaries in entities
class EmailState(BaseModel):
    email_body: str
    category: Optional[str] = None
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None  # ✅ Now allows nested dicts
    reply: Optional[str] = None

# Prompt to classify emails
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify this email as one of the following: support, schedule, billing, feedback, or other."),
    ("human", "{email_body}")
])

# Prompt to extract intent and entities
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract intent and key named entities (e.g., names, dates, times) from the following email. Return a valid JSON object with 'intent' and 'entities'."),
    ("human", "{email_body}")
])

# Prompt to generate reply
reply_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant replying to a {category} email with the intent of {intent}. Use this context: {entities}"),
    ("human", "{email_body}")
])

# LLM initialization
llm = ChatOpenAI(api_key=api_key, temperature=temperature)

# Node 1: classify
def classify_email(state: EmailState) -> EmailState:
    try:
        result = safe_api_call(llm.invoke, classification_prompt.format(email_body=state.email_body))
        return EmailState(email_body=state.email_body, category=result.content.strip())
    except Exception as e:
        # Fallback to a default category if classification fails
        return EmailState(email_body=state.email_body, category="other")

# Node 2: extract intent + entities
def extract_entities_intent(state: EmailState) -> EmailState:
    try:
        result = safe_api_call(llm.invoke, extraction_prompt.format(email_body=state.email_body))
        try:
            parsed = json.loads(result.content)
        except json.JSONDecodeError:
            # Fallback parsing if JSON is malformed
            parsed = {"intent": "unknown", "entities": {}}
    except Exception as e:
        # Fallback values if API call fails
        parsed = {"intent": "unknown", "entities": {}}
    
    return EmailState(
        email_body=state.email_body,
        category=state.category,
        intent=parsed.get("intent", "unknown"),
        entities=parsed.get("entities", {})
    )

# Node 3: generate reply
def generate_reply(state: EmailState) -> EmailState:
    try:
        result = safe_api_call(llm.invoke, reply_prompt.format(
            email_body=state.email_body,
            category=state.category,
            intent=state.intent,
            entities=state.entities
        ))
        reply_content = result.content.strip()
    except Exception as e:
        # Fallback reply if generation fails
        reply_content = f"I apologize, but I'm unable to generate a proper reply at the moment. Please contact support for assistance with your {state.category} inquiry."
    
    return EmailState(
        email_body=state.email_body,
        category=state.category,
        intent=state.intent,
        entities=state.entities,
        reply=reply_content
    )

# Build LangGraph
def build_email_graph():
    graph = StateGraph(EmailState)
    graph.add_node("classify_email", RunnableLambda(classify_email))
    graph.add_node("extract_entities_intent", RunnableLambda(extract_entities_intent))
    graph.add_node("generate_reply", RunnableLambda(generate_reply))
    graph.set_entry_point("classify_email")
    graph.add_edge("classify_email", "extract_entities_intent")
    graph.add_edge("extract_entities_intent", "generate_reply")
    graph.set_finish_point("generate_reply")
    return graph.compile()
