# ==============================================================================
# Copyright 2024 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""Module that defines default LLM configurations for the Langchain Agent."""

from langchain_google_vertexai import ChatVertexAI, VertexAI, HarmBlockThreshold, HarmCategory
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextGenerationModel

base_maestro_chat_llm = ChatVertexAI(
    model_name='gemini-1.0-pro-001', # note: 'gemini-1.0-pro' -> defaults to pro-002
    temperature=0,
    top_p=1.0,
    top_k=1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    },
    convert_system_message_to_human=True
)

base_maestro_llm = VertexAI(
    model_name='gemini-1.0-pro-001', # note: 'gemini-1.0-pro' -> defaults to pro-002
    temperature=0,
    top_p=1.0,
    top_k=1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    },
    convert_system_message_to_human=True
)

text_bison_model = TextGenerationModel.from_pretrained('text-bison')
gemini_model = VertexAI(
    model_name='gemini-1.0-pro-001',
    temperature=0.4,
    top_p=1.0,
    top_k=1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    }
)
