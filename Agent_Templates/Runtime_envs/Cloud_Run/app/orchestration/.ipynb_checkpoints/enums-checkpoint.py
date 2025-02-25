# ==============================================================================
# Copyright 2024 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

from enum import Enum

class UserRoles(Enum):
    """Enum representing the available user roles options."""

    SALESFORCE_USER_ROLE = 'salesforce_user'
    READONLY_USER_ROLE = 'readonly_user'

class AgentTypes(Enum):
    """Enum representing the available Langchain agent options."""
    
    LANGCHAIN_TOOL_CALLING_AGENT = 'langchain_tool_calling_agent'
    LANGCHAIN_REACT_AGENT = 'langchain_react_agent'
    LANGCHAIN_STRUCTURED_CHAT_AGENT = 'langchain_structured_chat_agent'
