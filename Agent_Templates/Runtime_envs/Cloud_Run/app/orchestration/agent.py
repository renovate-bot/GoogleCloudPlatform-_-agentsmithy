# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""Module used to define and interact with agent orchestrators."""

import langchain
from langgraph.prebuilt import create_react_agent
from vertexai.generative_models import ResponseValidationError
from vertexai.preview import reasoning_engines

from app.orchestration.constants import (
    GEMINI_FLASH_20_LATEST
)
from app.orchestration.enums import (
    OrchestrationFramework
)
from app.orchestration.tools import get_maestro_tools
from app.orchestration.models import (
    get_model_obj_from_string
)


class AgentManager():
    """Class that constructs and manages an Agent Executor"""

    def __init__(
        self,
        orchestration_framework: str = OrchestrationFramework.LANGCHAIN_REACT_AGENT.value,
        model_name: str = GEMINI_FLASH_20_LATEST,
        return_steps: bool = False,
        verbose: bool = True) -> langchain.agents.agent.AgentExecutor:
        """Constructs a custom agent with the specified configuration.

        Args:
            agent_type: The type of agent to use.
            base_llm: The LLM to use for the  agent.
            return_steps: Whether to return the agent's trajectory of intermediate
                steps at the end in addition to the final output.
            verbose: Whether or not run in verbose mode. In verbose mode, some intermediate
                logs will be printed to the console.
        """
        # self.tools = get_maestro_tools(user_role=maestro_user_role)
        self.model_name = model_name
        self.model_obj = get_model_obj_from_string(self.model_name)

        match orchestration_framework:
            case OrchestrationFramework.LANGCHAIN_REACT_AGENT.value:
                self.agent_executor = create_react_agent(
                    model=self.model_obj, 
                    tools=self.tools,
                    debug=verbose
                )
            case OrchestrationFramework.VERTEX_AI_REASONING_ENGINE_LANCHAIN_AGENT.value:
                self.agent_executor = reasoning_engines.LangchainAgent(
                    model=self.model_name,
                    model_kwargs={'temperature': 0},
                    tools=self.tools,
                    agent_executor_kwargs={'return_intermediate_steps': return_steps}
                )
            case _:
                raise ValueError(f'Orchestration Framework {OrchestrationFramework} is not currently supported.')


    def invoke(self,
               prompt: str,
               session_id: str,
               stream: bool = False,
               ignore_response_validation: bool = True,
               max_retries: int = 10) -> list:
        """Invokes the Agent.

        Args:
            prompt: The end-user question that was asked.
            session_id: The session id.
            stream: Boolean determining whether to stream response or use invoke directly.
            ignore_response_validation: When to retry again if a ResponseValidationError 
                is encountered.
            max_retries: Max number of retries if a ResponseValidationError is encountered.
        """
        response = []
        input_prompt = {'input': prompt}
        config = {'configurable': {'session_id': session_id}}

        if ignore_response_validation:
            for _ in range(max_retries):
                try:
                    if stream:
                        response = self.agent_executor.stream(
                            input_prompt, 
                            config=config)
                    else:
                        response = self.agent_executor.invoke(
                            input_prompt, 
                            config=config)
                    break
                except ResponseValidationError as e:
                    # Try again
                    print(f'Issue encountered {e}')
                    pass

            if not response:
                raise Exception(f'Max retries reached, please check you prompt before trying again.')
        else:
            try:
                if stream:
                    response = self.agent_executor.stream(
                        input_prompt, 
                        config=config)
                else:
                    response = self.agent_executor.invoke(
                        input_prompt, 
                        config=config)
            except Exception as e:
                raise Exception(f'An error occurred when calling the agent. {e}')

        return response
