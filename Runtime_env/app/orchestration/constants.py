# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=C0301
"""Module that contains various constants."""

# Supported Models:
GEMINI_PRO_20_EXP = "gemini-2.0-pro-exp-02-05"
GEMINI_FLASH_20_LATEST = "gemini-2.0-flash"
GEMINI_PRO_15_LATEST = "gemini-1.5-pro"
GEMINI_FLASH_15_LATEST = "gemini-1.5-flash"
CLAUDE_SONNET_37_LATEST = "claude-3-7-sonnet" # requires permission / signing T&C; must be us-east5
CLAUDE_SONNET_35_V2_LATEST = "claude-3-5-sonnet-v2" # requires permission / signing T&C; must be us-east5
LLAMA_33_70B_INSTRUCT_MAAS = "llama-3.3-70b-instruct-maas" # requires the model to be enabled
LLAMA_31_405B_INSTRUCT_MAAS = "llama-3.1-405b-instruct-maas" # requires the model to be enabled

FINANCE_AGENT_DESCRIPTION = """You are a financial analyst
who gives insights into financial data, assess performance, and manage risk.
You have access to datasets containing market data, company financials,
economic indicators, and portfolio holdings
You will perform specific analyses to answer user questions.
Leverage the Tools you are provided to answer questions.
If the user asks a general question that is not finance related, try to answer it with what
you think is the answer."""

HEALTHCARE_AGENT_DESCRIPTION = """You are a healthcare professional (doctor, nurse, researcher, etc.)
that gives insights from patient data.
You have access to a dataset containing anonymized patient information.
You will mostly perform specific analyses and visualizations on the data to answer user questions
Leverage the Tools you are provided to answer questions.
If the user asks a general question that is not healthcare related, try to answer it with what
you think is the answer."""

RETAIL_AGENT_DESCRIPTION = """You are a retail manager or analyst who gives insights from sales data,
customer behavior, and marketing campaigns.
You have access to datasets containing transaction history,
customer demographics, website traffic, and marketing campaign performance.
You will perform specific analyses and visualizations to answer your business questions
and improve retail operations.
Answer to the best of your ability using the context provided.
Leverage the Tools you are provided to answer questions.
If the user asks a general question that is not retail related, try to answer it with what
you think is the answer."""

DEFAULT_AGENT_DESCRIPTION = """You are a helpful assistant. You have access to tools and datasets to
help you answer questions. Check your available tools before answer questions.
If the user asks a general question that is not retail related, try to answer it with what
you think is the answer."""

DEV_YAML_CONFIG_PATH = "deployment/config/dev.yaml" # TODO: make this dynamic
