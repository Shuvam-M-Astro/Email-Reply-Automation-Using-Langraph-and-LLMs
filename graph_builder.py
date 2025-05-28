from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from utils import load_config
from typing import Optional

# Load config from YAML
config = load_config()
api_key = config["openai_api_key"]
temperature = config.get("model_temperature", 0.3)

# Define LangGraph state schema using Pydantic
class EmailState(BaseModel):
    email_body: str
    reply: Optional[str] = None  # ✅ allow graph to fill this in
    
# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant replying to emails."),
    ("human", "{email_body}")
])

# Initialize the language model
llm = ChatOpenAI(api_key=api_key, temperature=temperature)

# Function to generate email reply
def generate_email_reply(state: EmailState) -> EmailState:
    result = llm.invoke(prompt.format(email_body=state.email_body))
    return EmailState(email_body=state.email_body, reply=result.content)

# Build and return compiled LangGraph
def build_email_graph():
    graph = StateGraph(EmailState)
    graph.add_node("generate_reply", RunnableLambda(generate_email_reply))
    graph.set_entry_point("generate_reply")
    graph.set_finish_point("generate_reply")

    return graph.compile()
