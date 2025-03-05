# TODO: delete this file after verifying successful deployment

import vertexai

from app.orchestration.config import (
    AGENT_INDUSTRY_TYPE,
    PROJECT_ID,
    VERTEX_AI_LOCATION,
    GCS_STAGING_BUCKET
)
from app.orchestration.utils import get_agent_from_config

vertexai.init(
    project=PROJECT_ID,
    location=VERTEX_AI_LOCATION,
    staging_bucket=GCS_STAGING_BUCKET
)

# Get agent based on user selection
agent_manager = get_agent_from_config(
    # agent_orchestration_framework=AGENT_ORCHESTRATION_FRAMEWORK,
    agent_orchestration_framework='langchain_vertex_ai_reasoning_engine_agent',
    industry_type=AGENT_INDUSTRY_TYPE,
)

agent_manager.deploy_agent()
