import google
import os
import vertexai
from langchain_core.documents import Document
from langchain_core.tools import tool
from typing import List

from app.rag.templates import format_docs
from app.rag.retriever import get_compressor, get_retriever

VERTEX_AI_LOCATION = os.getenv("REGION", "us-central1")
AGENT_BUILDER_LOCATION = os.getenv("AGENT_BUILDER_LOCATION", "us")
DATA_STORE_ID = os.getenv("DATA_STORE_ID", "sample-datastore")

# Initialize Google Cloud and Vertex AI
credentials, project_id = google.auth.default()
vertexai.init(project=project_id)


retriever = get_retriever(
    project_id=project_id,
    data_store_id=DATA_STORE_ID,
    agent_builder_location=AGENT_BUILDER_LOCATION,
)
compressor = get_compressor(project_id=project_id)

@tool(response_format="content_and_artifact")
def retrieve_docs(query: str) -> tuple[str, List[Document]]:
    """
    Useful for retrieving relevant documents based on a query.
    Use this when you need additional information to answer a question.

    Args:
        query (str): The user's question or search query.

    Returns:
        List[Document]: A list of the top-ranked Document objects, limited to TOP_K (5) results.
    """
    # Use the retriever to fetch relevant documents based on the query
    retrieved_docs = retriever.invoke(query)
    # Re-rank docs with Vertex AI Rank for better relevance
    ranked_docs = compressor.compress_documents(documents=retrieved_docs, query=query)
    # Format ranked documents into a consistent structure for LLM consumption
    formatted_docs = format_docs.format(docs=ranked_docs)
    return (formatted_docs, ranked_docs)


@tool
def should_continue() -> None:
    """
    Use this tool if you determine that you have enough context to respond to the questions of the user.
    """
    return None


tools = [retrieve_docs, should_continue]