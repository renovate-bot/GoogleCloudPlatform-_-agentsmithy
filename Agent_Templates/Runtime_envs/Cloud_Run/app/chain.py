from typing import Any, AsyncIterator, Dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_vertexai import ChatVertexAI

from app.industries.finance import PROMPT
#from app.industries.health import PROMPT
#from app.industries.retail import PROMPT

from app.rag.templates import inspect_conversation_template
from app.rag.tool import retrieve_docs, should_continue, tools
from app.utils.decorators import custom_chain
from app.utils.output_types import OnChatModelStreamEvent, OnToolEndEvent

LOCATION = "us-central1"
LLM = "gemini-1.5-flash-002"

llm = ChatVertexAI(
    model_name=LLM,
    location=LOCATION,
    temperature=0,
    max_output_tokens=1024,
)

inspector = inspect_conversation_template  | llm.bind_tools(
    tools, tool_choice="any"
)

# Set up response chain
response_chain = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PROMPT,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
) | llm


@custom_chain
async def chain(
    input: Dict[str, Any], **kwargs: Any
) -> AsyncIterator[OnToolEndEvent | OnChatModelStreamEvent]:
    """
    Implement a RAG QA chain with tool calls.

    This function is decorated with `custom_chain` to offer LangChain compatible
    astream_events, support for synchronous invocation through the `invoke` method,
    and OpenTelemetry tracing.
    """
    # Inspect conversation and determine next action
    inspection_result = inspector.invoke(input)
    tool_call_result = inspection_result.tool_calls[0]

    selected_tool = {"retrieve_docs": retrieve_docs, "should_continue": should_continue}[tool_call_result["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call_result)
    input["messages"].append(inspection_result)
    input["messages"].append(tool_msg)

    print(input["messages"])

    # Yield tool results metadata
    yield OnToolEndEvent(
        data={"input": tool_call_result["args"], "output": tool_msg}
    )

    # Stream LLM response
    async for chunk in response_chain.astream(input=input):
        yield OnChatModelStreamEvent(data={"chunk": chunk})