# TODO: delete this file after verifying successful deployment

import vertexai

from app.orchestration.agent import deploy_agent_to_agent_engine
from app.orchestration.config import (
    AGENT_INDUSTRY_TYPE,
    AGENT_ORCHESTRATION_FRAMEWORK,
    PROJECT_ID,
    VERTEX_AI_LOCATION,
    GCS_STAGING_BUCKET
)
from app.orchestration.server_utils import get_agent_from_config

vertexai.init(
    project=PROJECT_ID,
    location=VERTEX_AI_LOCATION,
    staging_bucket=GCS_STAGING_BUCKET
)

# Get agent based on user selection
agent_manager = get_agent_from_config(
    agent_orchestration_framework=AGENT_ORCHESTRATION_FRAMEWORK,
    industry_type=AGENT_INDUSTRY_TYPE,
)

deploy_agent_to_agent_engine(agent_manager)

# from vertexai import agent_engines
# from vertexai.preview import reasoning_engines

# for engine in reasoning_engines.ReasoningEngine.list():
#     engine.delete()

# print(reasoning_engines.ReasoningEngine.list())
