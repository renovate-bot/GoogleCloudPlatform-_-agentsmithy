# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""Module used to define and interact with agent orchestrators."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, Optional

from google.api_core import exceptions
from langchain.agents import (
    AgentExecutor,
    create_react_agent as langchain_create_react_agent
)
from langchain_core.messages import AIMessageChunk, ToolMessage, AIMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent as langgraph_create_react_agent
from vertexai.preview import reasoning_engines # TODO: update this when it becomes agent engine
from vertexai import agent_engines

from app.orchestration.constants import (
    GEMINI_FLASH_20_LATEST,
)
from app.orchestration.config import (
    USER_AGENT,
    AGENT_DESCRIPTION
)
from app.orchestration.enums import OrchestrationFramework
from app.orchestration.tools import get_tools
from app.utils.utils import (
    get_requirements_from_toml,
)
# from app.utils.output_types import OnChatModelStreamEvent, ChatModelStreamData


class BaseAgentManager(ABC):
    """
    Abstract base class for Agent Managers.  Defines the common interface
    for creating and managing agent executors with different orchestration
    frameworks.
    """

    def __init__(
        self,
        prompt: str,
        industry_type: str,
        orchestration_framework: str,
        model_name: str,
        max_retries: int,
        max_output_tokens: int,
        temperature: float,
        top_p: float,
        top_k: int,
        return_steps: bool,
        verbose: bool
    ):
        """
        Initializes the BaseAgentManager with common configurations.

        Args:
            prompt: System instructions to give to the agent.
            industry_type: The agent industry type to use. Correlates to tool configs.
            orchestration_framework: The type of agent framework to use.
            model_name: The valid name of the LLM to use for the agent.
            max_retries: Maximum number of times to retry the query on a failure.
            max_output_tokens: Maximum amount of text output from one prompt.
            temperature: Temperature to use for the agent.
            top_p: Top p value. Chooses the words based on a cumulative probability threshold.
            top_k: Top k value. Chooses the top k most likely words
            return_steps: Whether to return the agent's trajectory of intermediate
                steps at the end in addition to the final output.
            verbose: Whether or not run in verbose mode.
        """
        self.prompt = prompt
        self.industry_type = industry_type
        self.orchestration_framework = orchestration_framework
        self.model_name = model_name
        self.max_retries = max_retries
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.return_steps = return_steps
        self.verbose = verbose

        self.tools = self.get_tools()
        self.model_obj = self.get_model_obj()
        self.agent_executor = self.create_agent_executor()


    @abstractmethod
    def create_agent_executor(self):
        """
        Abstract method to create the specific agent executor based on the
        orchestration framework.  This must be implemented by subclasses.

        Returns:
            The initialized agent executor instance.
        """
        pass


    def get_tools(self):
        """
        Helper method to retrieve tools based on the industry type.

        Returns:
            A list of tools for the agent to use, based on the industry type.
        """
        return get_tools(
            self.industry_type,
            self.orchestration_framework
        )


    def get_model_obj(self):
        """
        Helper method to retrieve the model object based on the model name 
        and config.

        Returns:
            An LLM object for the Agent to use.

        Exception:
            The model_name is not found.
        """
        try:
            return ChatVertexAI(
                model_name=self.model_name,
                max_retries=self.max_retries,
                max_output_tokens=self.max_output_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k,
                verbose=self.verbose
            )
        except exceptions.NotFound as e:
            raise exceptions.NotFound(f"Resource not found. {e}")
        except Exception as e:
            raise RuntimeError(f"Error encountered initalizing model resource. {e}") from e


    @abstractmethod
    async def astream(
        self,
        input: Dict[str, Any],
    ) -> AsyncGenerator[Dict, Any]:
        """
        Abstract method to asynchronously stream the Agent output.
        This should be implemented by subclasses to handle the specific
        streaming logic of their agent executor.
        """
        pass


class LangChainPrebuiltAgentManager(BaseAgentManager):
    """
    AgentManager subclass for LangChain Agent orchestration.
    """
    def __init__(
        self,
        prompt: str,
        industry_type: str,
        model_name: Optional[str] = GEMINI_FLASH_20_LATEST,
        max_retries: Optional[int] = 6,
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = 0,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        return_steps: Optional[bool] = False,
        verbose: Optional[bool] = True
    ):
        super().__init__(
            prompt=prompt,
            industry_type=industry_type,
            orchestration_framework=OrchestrationFramework.LANGCHAIN_PREBUILT_AGENT.value,
            model_name=model_name,
            max_retries=max_retries,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            return_steps=return_steps,
            verbose=verbose
        )


    def create_agent_executor(self):
        """
        Creates a Langchain React Agent executor.
        """
        react_agent = langchain_create_react_agent(
            prompt=self.prompt,
            llm=self.model_obj,
            tools=self.tools,
        )
        return AgentExecutor(
            agent=react_agent,
            tools=self.tools,
            return_intermediate_steps=self.return_steps,
            verbose=self.verbose
        )


    async def astream(
        self,
        input: Dict[str, Any],
    ) -> AsyncGenerator[Dict, Any]:
        """Asynchronously event streams the Agent output.

        Args:
            input: The list of messages to send to the model as input.

        Yields:
            Dictionaries representing the streamed agent output.

        Exception:
            An error is encountered during streaming.
        """
        try:
            async for chunk in self.agent_executor.astream(
                {
                    "input": input["messages"][0],
                    "chat_history": input["messages"][1:],
                }
            ):
                # Organize response object to be consistent with other Agents (e.g. Agent Engine)
                if "output" in chunk:
                    response_obj = {
                        "agent": {
                            "output": chunk["output"],
                            "messages": [
                                {
                                    "lc": 1,
                                    "type": "constructor",
                                    "id": ["langchain", "schema", "messages", "AIMessage"],
                                    "kwargs": {
                                        "content": chunk["output"],
                                        "type": "ai",
                                        "tool_calls": [],
                                        "invalid_tool_calls": [],
                                        "id": input["run_id"]
                                    }
                                }
                            ]
                        }
                    }
                    yield response_obj
            return  # Exit the loop if successful
        except Exception as e:
            raise RuntimeError(f"Unexpected error. {e}") from e


class LangGraphPrebuiltAgentManager(BaseAgentManager):
    """
    AgentManager subclass for LangGraph Agent orchestration.
    """
    def __init__(
        self,
        prompt: str,
        industry_type: str,
        model_name: Optional[str] = GEMINI_FLASH_20_LATEST,
        max_retries: Optional[int] = 6,
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = 0,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        return_steps: Optional[bool] = False,
        verbose: Optional[bool] = True
    ):
        super().__init__(
            prompt=prompt,
            industry_type=industry_type,
            orchestration_framework=OrchestrationFramework.LANGGRAPH_PREBUILT_AGENT.value,
            model_name=model_name,
            max_retries=max_retries,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            return_steps=return_steps,
            verbose=verbose
        )


    def create_agent_executor(self):
        """
        Creates a LangGraph React Agent executor.
        """
        return langgraph_create_react_agent(
            prompt=self.prompt,
            model=self.model_obj,
            tools=self.tools,
            debug=self.verbose
        )


    async def astream(
        self,
        input: Dict[str, Any],
    ) -> AsyncGenerator[Dict, Any]:
        """Asynchronously event streams the Agent output.

        Args:
            input: The list of messages to send to the model as input.

        Yields:
            Dictionaries representing the streamed agent output.

        Exception:
            An error is encountered during streaming.
        """
        try:
            async for chunk in self.agent_executor.astream(input, stream_mode="values"):
                message = chunk["messages"][-1]
                if isinstance(message, AIMessage):
                    # Organize response object to be consistent with other Agents (e.g. Agent Engine)
                    response_obj = {
                        "agent": {
                            "messages": [
                                {
                                    "lc": 1,
                                    "type": "constructor",
                                    "id": ["langgraph", "schema", "messages", "AIMessage"],
                                    "kwargs": {
                                        "content": message.content,
                                        "type": "ai",
                                        "tool_calls": [],
                                        "invalid_tool_calls": [],
                                        "id": input["run_id"]
                                    },
                                    "usage_metadata": message.usage_metadata
                                }
                            ]
                        }
                    }
                    yield response_obj
            return  # Exit the loop if successful
        except Exception as e:
            raise RuntimeError(f"Unexpected error. {e}") from e


class LangChainVertexAIReasoningEngineAgentManager(BaseAgentManager):
    """
    AgentManager subclass for Vertex AI Reasoning Engine LangChain orchestration.
    """
    def __init__(
        self,
        prompt: str,
        industry_type: str,
        model_name: Optional[str] = GEMINI_FLASH_20_LATEST,
        max_retries: Optional[int] = 6,
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = 0,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        return_steps: Optional[bool] = False,
        verbose: Optional[bool] = True
    ):
         super().__init__(
            prompt=prompt,
            industry_type=industry_type,
            orchestration_framework=OrchestrationFramework.LANGCHAIN_VERTEX_AI_REASONING_ENGINE_AGENT.value,
            model_name=model_name,
            max_retries=max_retries,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            return_steps=return_steps,
            verbose=verbose
        )


    def create_agent_executor(self):
        """
        Creates a Vertex AI Reasoning Engine Langchain Agent executor.
        """
        langchain_agent = reasoning_engines.LangchainAgent(
            prompt=self.prompt,
            model=self.model_name,
            tools=self.tools,
            agent_executor_kwargs={
                'return_intermediate_steps': self.return_steps,
                'verbose': self.verbose
            },
            enable_tracing=True
        )
        langchain_agent.set_up()
        return langchain_agent


    async def astream(
        self,
        input: Dict[str, Any],
    ) -> AsyncGenerator[Dict, Any]:
        """
        Asynchronously streams the Agent output using Vertex AI reasoning engine.

        Args:
            input: The list of messages to send to the model as input.

        Yields:
            Dictionaries representing the streamed agent output.

        Exception:
            An error is encountered during streaming.
        """
        try:
            for chunk in self.agent_executor.stream_query(
                input=input
            ):
                # Set the run_ids using the one from the server
                chunk["messages"] = [{**msg, "kwargs": {**msg["kwargs"], "id": input["run_id"]}} for msg in chunk["messages"]]
                yield {"agent": chunk}
        except Exception as e:
            raise RuntimeError(f"Unexpected error. {e}") from e


class LangGraphVertexAIReasoningEngineAgentManager(BaseAgentManager):
    """
    AgentManager subclass for Vertex AI Reasoning Engine LangGraph orchestration.
    """
    def __init__(
        self,
        prompt: str,
        industry_type: str,
        model_name: Optional[str] = GEMINI_FLASH_20_LATEST,
        max_retries: Optional[int] = 6,
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = 0,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        return_steps: Optional[bool] = False,
        verbose: Optional[bool] = True
    ):
         super().__init__(
            prompt=prompt,
            industry_type=industry_type,
            orchestration_framework=OrchestrationFramework.LANGGRAPH_VERTEX_AI_REASONING_ENGINE_AGENT.value,
            model_name=model_name,
            max_retries=max_retries,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            return_steps=return_steps,
            verbose=verbose
        )


    def create_agent_executor(self):
        """
        Creates a Vertex AI Reasoning Engine LangGraph Agent executor.
        """
        langgraph_agent = reasoning_engines.LanggraphAgent(
            model=self.model_name,
            tools=self.tools,
            runnable_kwargs={"prompt": self.prompt, "debug": self.verbose},
            enable_tracing=True
        )
        langgraph_agent.set_up()
        return langgraph_agent


    async def astream(
        self,
        input: Dict[str, Any],
    ) -> AsyncGenerator[Dict, Any]:
        """
        Asynchronously streams the Agent output using Vertex AI reasoning engine.

        Args:
            input: The list of messages to send to the model as input.

        Yields:
            Dictionaries representing the streamed agent output.

        Exception:
            An error is encountered during streaming.
        """
        try:
            for chunk in self.agent_executor.stream_query(
                input=input,
                stream_mode="values"
            ):
                # Override the each of the run_ids with the one from the server
                chunk["messages"] = [{**msg, "kwargs": {**msg["kwargs"], "id": input["run_id"]}} for msg in chunk["messages"]]
                yield {"agent": chunk}
        except Exception as e:
            raise RuntimeError(f"Unexpected error. {e}") from e


def deploy_agent_to_agent_engine(
    agent_manager: BaseAgentManager
):
    """
    Deploys the Vertex AI agent engine to a remote managed endpoint.

    Args:
        agent_manager: The agent_manager to be deployed to agent engine.

    Returns:
        Remote Agent Engine agent.

    Exception:
        An error is encountered during deployment.
    """
    try:
        remote_agent = agent_engines.create(
            agent_manager.agent_executor,
            requirements=get_requirements_from_toml(),
            display_name=USER_AGENT,
            description=AGENT_DESCRIPTION,
            extra_packages=["./app", "./deployment/config"],
        )
    except Exception as e:
        raise RuntimeError(f"Error deploying Agent Engine Agent. {e}") from e

    return remote_agent
