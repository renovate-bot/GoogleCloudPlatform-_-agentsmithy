# ==============================================================================
# Copyright 2024 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""Module used to define and interact with langchain-based agents."""

import json
from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List, Tuple, Union

import langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_react_agent, create_structured_chat_agent
from langchain.agents.output_parsers.react_json_single_input import ReActJsonSingleInputOutputParser
from langchain.memory import ChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, messages_to_dict
import langchain_core
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory 
from vertexai.generative_models import ResponseValidationError

from decision_component.enums import(
    AgentTypes,
    UserRoles
)
from decision_component.prompts import (
    tool_calling_agent_prompt,
    react_agent_prompt_v2,
    react_agent_prompt_json
)
from decision_component.tools import get_maestro_tools
from decision_component.models import (
    base_maestro_chat_llm,
    base_maestro_llm,
    gemini_model,
    text_bison_model
)

class ConversationBufferSlidingWindow(BaseChatMessageHistory):
    """A chat message history that only keeps the last K messages."""

    def __init__(self, buffer_size: int):
        super().__init__()
        self.buffer_size = buffer_size
        self.messages: List[BaseMessage] = []

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store, keeping only the last K."""
        self.messages.extend(messages)
        # Ensure only the last K messages are kept
        self.messages = self.messages[-self.buffer_size:]

    def clear(self):
        self.messages = []


class Agent():
    """Class that constructs and maintains a langchain RunnableWithMessageHistory"""

    def __init__(
        self,
        agent_type: str = AgentTypes.LANGCHAIN_REACT_AGENT.value,
        base_llm: langchain_core.language_models.base.BaseLanguageModel = base_maestro_llm,
        handle_parsing_errors: bool = True,
        maestro_user_role: str = UserRoles.READONLY_USER_ROLE.value,
        memory_window_size: int = 10,
        parser: langchain_core.output_parsers.base.BaseOutputParser = None,
        prompt: langchain_core.prompts.prompt.PromptTemplate = react_agent_prompt_v2,
        return_intermediate_steps: bool = False,
        verbose: bool = True) -> langchain.agents.agent.AgentExecutor:
        """Constructs a custom agent with the specified configuration. See for more details:
            https://python.langchain.com/docs/expression_language/how_to/message_history/

        Args:
            agent_type: The type of Langchain agent to use. See for more details:
                https://python.langchain.com/docs/modules/agents/agent_types/
            base_llm: The LLM to use for the  agent.
            handle_parsing_errors: How to handle errors raised by the agent’s output parser. 
                Defaults to False, which raises the error. If true, the error will be sent 
                back to the LLM as an observation.
            maestro_user_role: The entitlements access level of the agent
            memory_window_size: The maximum number of messages to keep in the buffer at any time.
                Defaults to 20 messages (10 turns of a conversation)
            parser: The output parser used in the agent.
            prompt: The prompt for the base_llm to run.
            return_intermediate_steps: Whether to return the agent’s trajectory of intermediate
                steps at the end in addition to the final output.
            verbose: Whether or not run in verbose mode. In verbose mode, some intermediate
                logs will be printed to the console.
        """
        self.stateful_memory = {}
        self.memory_window_size = memory_window_size
        self.tools = get_maestro_tools(user_role=maestro_user_role)

        match agent_type:
            case AgentTypes.LANGCHAIN_TOOL_CALLING_AGENT.value:
                self.agent_runnable = create_tool_calling_agent(base_llm, 
                                                                self.tools,
                                                                prompt,
                                                                output_parser=parser)
            case AgentTypes.LANGCHAIN_REACT_AGENT.value:
                self.agent_runnable = create_react_agent(base_llm, 
                                                         self.tools,
                                                         prompt,
                                                         output_parser=parser)
            case AgentTypes.LANGCHAIN_STRUCTURED_CHAT_AGENT.value:
                self.agent_runnable = create_structured_chat_agent(base_llm, 
                                                                   self.tools,
                                                                   prompt)
            case _:
                raise ValueError(f'Agent type {agent_type} is not currently supported.')
        
        agent_executor = AgentExecutor(
            agent=self.agent_runnable,
            tools=self.tools,
            verbose=verbose,
            handle_parsing_errors=handle_parsing_errors,
            return_intermediate_steps=return_intermediate_steps)

        self.agent_executor_with_message_history = RunnableWithMessageHistory(
            runnable=agent_executor,
            get_session_history=self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history")


    def call(self,
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
                        response = self.agent_executor_with_message_history.stream(
                            input_prompt, 
                            config=config)
                    else:
                        response = self.agent_executor_with_message_history.invoke(
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
                    response = self.agent_executor_with_message_history.stream(
                        input_prompt, 
                        config=config)
                else:
                    response = self.agent_executor_with_message_history.invoke(
                        input_prompt, 
                        config=config)
            except Exception as e:
                raise Exception(f'An error occurred when calling the agent. {e}')

        return response

    
    def get_session_history(
        self,
        session_id: str,
        to_json: bool = False) -> BaseChatMessageHistory | str:
        """Gets the chat history of the agent for a given session id

        Args:
            session_id: The session id.
            to_json: Boolean that decides whether to return as a json string.
        """
        if session_id not in self.stateful_memory:
            self.stateful_memory[session_id] = ConversationBufferSlidingWindow(buffer_size=self.memory_window_size)
        if to_json:
            return json.dumps(messages_to_dict(self.stateful_memory[session_id].messages))
        return self.stateful_memory[session_id]


    def set_session_history(
        self,
        session_id: str,
        starting_message_history: List[Union[langchain_core.messages.human.HumanMessage,
                                             langchain_core.messages.ai.AIMessage]]):
        """Sets the chat history of the agent for a given session id
        
        Args:
            session_id: The session id.
            starting_message_history: List chat messages to initialize the Agent' session id with.
        """
        try:
            self.stateful_memory[session_id] = ChatMessageHistory(messages=starting_message_history)
        except Exception as e:
            raise Exception(f'starting_message_history is not formatted correctly. {e}')


    def clear_session_history(
        self,
        session_id: str):
        """Deletes the chat history of the agent for a given session id
        
        Args:
            session_id: The session id.
        """
        if session_id in self.stateful_memory:
            self.stateful_memory[session_id].clear()


    def create_session_title(
        self,
        session_id: str) -> str:
        """Takes the session id chat history of the agent and turns it into a short title
        
        Args:
            session_id: The session id.
        """
        history = self.get_session_history(session_id=session_id, to_json=True)
        return gemini_model.invoke(f'Give me a title for this conversation: {history}')


    def create_session_summary(
        self,
        session_id: str) -> str:
        """Takes the session id chat history of the agent and generates a summary

        Args:
            session_id: The session id.
        """
        history = self.get_session_history(session_id=session_id, to_json=True)
        return gemini_model.invoke(f'Give me a summary of this conversation: {history}')
