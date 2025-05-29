from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Optional
from utils import load_config

# Load API key and config
config = load_config()
api_key = config["openai_api_key"]
temperature = config.get("model_temperature", 0.3)

# Define LangGraph state schema
class EmailState(BaseModel):
    email_body: str
    category: Optional[str] = None
    reply: Optional[str] = None

# Define prompt templates
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify this email as one of the following: support, schedule, billing, feedback, or other."),
    ("human", "{email_body}")
])

reply_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant replying to a {category} email."),
    ("human", "{email_body}")
])

# Initialize LLM
llm = ChatOpenAI(api_key=api_key, temperature=temperature)

# Classification step
def classify_email(state: EmailState) -> EmailState:
    result = llm.invoke(classification_prompt.format(email_body=state.email_body))
    return EmailState(email_body=state.email_body, category=result.content.strip())

# Reply generation step
def generate_reply(state: EmailState) -> EmailState:
    result = llm.invoke(reply_prompt.format(email_body=state.email_body, category=state.category))
    return EmailState(email_body=state.email_body, category=state.category, reply=result.content.strip())

# Build LangGraph
def build_email_graph():
    graph = StateGraph(EmailState)
    graph.add_node("classify_email", RunnableLambda(classify_email))
    graph.add_node("generate_reply", RunnableLambda(generate_reply))
    graph.set_entry_point("classify_email")
    graph.add_edge("classify_email", "generate_reply")
    graph.set_finish_point("generate_reply")
    return graph.compile()
