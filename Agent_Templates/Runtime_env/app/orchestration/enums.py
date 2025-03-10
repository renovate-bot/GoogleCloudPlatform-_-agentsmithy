# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

from enum import Enum

class OrchestrationFramework(Enum):
    """Enum representing the available agent orchestration framework options."""

    LANGCHAIN_PREBUILT_AGENT = 'langchain_prebuilt_agent'
    LANGGRAPH_PREBUILT_AGENT = 'langgraph_prebuilt_agent'
    # LANGGRAPH_CUSTOM_AGENT = 'langgraph_custom_agent'
    LLAMA_AGENT = 'llama_agent'
    # CREW_AI_AGENT = 'crew_ai_agent' # Coming Soon
    # VERTEX_AI_AGENT_FRAMEWORK_AGENT = 'vertex_ai_agent_framework_agent' # Coming Soon

class IndustryType(Enum):
    """Enum representing the available Langchain agent options."""

    FINANCE_INDUSTRY = 'finance'
    RETAIL_INDUSTRY = 'retail'
    HEALTHCARE_INDUSTRY = 'healthcare'
