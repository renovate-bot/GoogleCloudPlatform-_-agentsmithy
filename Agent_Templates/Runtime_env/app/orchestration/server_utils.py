# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""Module that contains various utility functions."""
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from app.orchestration.agent import (
    LangChainPrebuiltAgentManager,
    LangGraphPrebuiltAgentManager,
    LangChainVertexAIReasoningEngineAgentManager,
    LangGraphVertexAIReasoningEngineAgentManager,
)
from app.orchestration.constants import (
    FINANCE_AGENT_DESCRIPTION,
    HEALTHCARE_AGENT_DESCRIPTION,
    RETAIL_AGENT_DESCRIPTION,
    DEFAULT_AGENT_DESCRIPTION
)
from app.orchestration.enums import (
    IndustryType,
    OrchestrationFramework
)


def get_init_prompt(
        agent_orchestration_framework: str,
        industry_type: str
) -> ChatPromptTemplate:
    """Creates the initialization prompt for the agent based on the industry."""

    if industry_type == IndustryType.FINANCE_INDUSTRY.value:
        sys_desc = FINANCE_AGENT_DESCRIPTION
    elif industry_type == IndustryType.HEALTHCARE_INDUSTRY.value:
        sys_desc = HEALTHCARE_AGENT_DESCRIPTION
    elif industry_type == IndustryType.RETAIL_INDUSTRY.value:
        sys_desc = RETAIL_AGENT_DESCRIPTION
    else:
        sys_desc = DEFAULT_AGENT_DESCRIPTION

    # The prebuilt langchain option is older and has a different prompt structure
    if agent_orchestration_framework ==OrchestrationFramework.LANGCHAIN_PREBUILT_AGENT.value:
        return PromptTemplate.from_template(sys_desc + '''You have access to the following tools:
                         
        TOOLS:
        ------

        Assistant has access to the following tools:

        {tools}

        To use a tool, please use the following format:

        ```
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ```

        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

        ```
        Thought: Do I need to use a tool? No
        Final Answer: [your response here]
        ```

        Begin!

        Previous conversation history:
        {chat_history}

        New input: {input}
        {agent_scratchpad}''')

    else:
        return ChatPromptTemplate.from_messages([
            ("system", f"{sys_desc}"),
            ("placeholder", "{messages}")
        ])

def get_agent_from_config(
        agent_orchestration_framework: str,
        industry_type: str,
    ):
    """Returns the associated Agent Manager based on the defined selection"""

    # Set up the agent backed on environment variables for user config
    init_prompt = get_init_prompt(agent_orchestration_framework, industry_type)

    # Set up agent type based on user config selection
    if agent_orchestration_framework == OrchestrationFramework.LANGCHAIN_PREBUILT_AGENT.value:
        agent_manager = LangChainPrebuiltAgentManager(
            prompt=init_prompt,
            industry_type=industry_type
        )
    elif agent_orchestration_framework == OrchestrationFramework.LANGCHAIN_VERTEX_AI_REASONING_ENGINE_AGENT.value:
        agent_manager = LangChainVertexAIReasoningEngineAgentManager(
            prompt=init_prompt,
            industry_type=industry_type
        )
    elif agent_orchestration_framework == OrchestrationFramework.LANGGRAPH_PREBUILT_AGENT.value:
        agent_manager = LangGraphPrebuiltAgentManager(
            prompt=init_prompt,
            industry_type=industry_type
        )
    elif agent_orchestration_framework == OrchestrationFramework.LANGGRAPH_VERTEX_AI_REASONING_ENGINE_AGENT.value:
        agent_manager = LangGraphVertexAIReasoningEngineAgentManager(
            prompt=init_prompt,
            industry_type=industry_type
        )
    else:
        # default agent orchestration is LangGraphPrebuiltAgentManager
        agent_manager = LangGraphPrebuiltAgentManager(
            prompt=init_prompt,
            industry_type=industry_type
        )

    return agent_manager
