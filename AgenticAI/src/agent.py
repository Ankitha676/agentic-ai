from typing import TypedDict, List
import pickle
from src.config import GROQ_MODEL, GROQ_API_KEY

from langgraph.graph import StateGraph
from langchain_groq import ChatGroq

from src.config import GROQ_MODEL, STRUCTURED_PATH
from src.retriever import hybrid_search, rerank


class AgentState(TypedDict):
    query: str
    retrieved_docs: List[str]
    structured_summary: str
    final_answer: str


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    groq_api_key=GROQ_API_KEY   # 🔥 THIS IS KEY FIX
)

with open(STRUCTURED_PATH, "rb") as f:
    structured_data = pickle.load(f)


def retrieve(state: AgentState):
    docs = hybrid_search(state["query"], k=8)
    ranked = rerank(state["query"], docs, llm)

    formatted = []
    for score, content, meta in ranked:
        formatted.append(f"""
Score: {score}
Source: {meta.get('source')} | Folder: {meta.get('folder')}

{content}
""")

    return {"retrieved_docs": formatted}


def analyze_structured(state: AgentState):
    summaries = []

    for df, file, folder in structured_data:
        if "status" in df.columns:
            violations = df[df["status"].astype(str).str.contains("FAIL", case=False)]
            summaries.append(f"{folder}/{file} → Violations: {len(violations)}")

    return {"structured_summary": "\n".join(summaries)}


def reason(state: AgentState):
    context = "\n\n".join(state["retrieved_docs"])
    structured = state["structured_summary"]

    prompt = f"""
You are an enterprise AI analyst.

Context:
{context}

Structured Data:
{structured}

Question:
{state['query']}

Provide:
- Final Answer
- Violations
- Evidence
- Missing Information
"""

    return {"final_answer": llm.invoke(prompt).content}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("structured", analyze_structured)
    graph.add_node("reason", reason)

    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "structured")
    graph.add_edge("structured", "reason")

    graph.set_finish_point("reason")

    return graph.compile()