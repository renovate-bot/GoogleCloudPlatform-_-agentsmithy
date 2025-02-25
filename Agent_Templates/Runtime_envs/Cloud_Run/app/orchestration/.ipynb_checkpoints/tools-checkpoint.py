# ==============================================================================
# Copyright 2024 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""Module that contains various Langchain tool definitions."""

from google.api_core.client_options import ClientOptions
from google.cloud import bigquery
from google.cloud import discoveryengine_v1 as discoveryengine
from langchain.agents import tool
from vertexai.generative_models import GenerationConfig, ResponseValidationError

from decision_component.constants import (
    CME_WEBSITE_SEARCH_ENG_ID,
    LOCATION,
    MAESTRO_INTRO,
    PROJECT_ID
)

from decision_component.enums import(
    UserRoles
)

from decision_component.models import (
    gemini_model,
    text_bison_model
)

from nl2sql.custom_prompt_chain import (
    NL2SQLAssistant
)

from rag.rag import (
    call_reports_rag
)

bq_client = bigquery.Client(project=PROJECT_ID) # Add in service_account


@tool(return_direct=True)
def fallback(question: str) -> str:
    """Use this tool for general questions that a large language model would know the answer to.

        Example questions:
        'Who is the President of France?'
        'What is a large language model?'

    """
    general_question_template = (f'{MAESTRO_INTRO}Please help employees at CME Group answer general knowledge questions. '
                                 f'question: {question}')
    return gemini_model.invoke(general_question_template)


@tool(return_direct=True)
def analyze_call_reports(question: str) -> str:
    """Answers questions related to customer calls, conversations, client meetings, or call reports.
        These questions usually provide some description about the particular clients or calls that
        need to be analyzed, and ask to do something with the information that matches the description
        (e.g. based on calls with ACME company, summarize their key pain points with product ABC).

        Supported data tables for this tool are as follows:

        Table Name | Table Description
        t_call_report__c | Data table showing the contents of all the calls from external leads/contacts who have called CME with a question or something to discuss.
    """
    response = call_reports_rag(question=question,
                                bq_client=bq_client,
                                gemini_model=gemini_model,
                                return_source_citations=False)
    return response


@tool(return_direct=True)
def query_database(question: str) -> str:
    """Answers questions that require analytical querying of a database. This tool
        should only be used if the question requires collecting information from a database.
        
        Supported data tables for this tool are as follow:
        
        Table Name | Table Description
        t_ga4_custom | Data table showing all of the digital activity that has occurred on the site for all webpages in the cmegroup domain
        t_lead | Data table showing a breakdown of all the leads that are registered with CME. A lead is someone who has not had any meaningful interactions with CME
        t_contact | Data table showing a breakdown of all the leads that are registered with CME. A contact is someone who has some meaningful interaction with CME (e.g. trading, frequent interactions on the cme website)
    """
    nl2sql_assistant = NL2SQLAssistant()

    citation_str, response, result, nl = nl2sql_assistant.gen_sql(question, sql2nl=True, insight=False)
    return f'{citation_str} {response} {result} {nl}'


# Todo: update this description
@tool
def google_search_tool(question: str) -> str:
    """Uses Google Search to gather information from the internet. 
        This tool should only be used as a last resort if real-time
        information cannot be retrieved using the other tools."
    """
    # search = GoogleSearchAPIWrapper()
    # search.run()
    response = 'The Google Search tool has not been implemented yet'
    return response


# Todo: update this description
@tool
def wolfram_alpha_tool(question: str) -> str:
    """Uses Wolfram Alpha to answer computational, mathematics, and graphing questions."""
    # wolfram = WolframAlphaAPIWrapper()
    # wolfram.run()
    response = 'The Wolfram Alpha tool has not been implemented yet'
    return response

@tool(return_direct=True)
def cme_info_lookup(question: str) -> str:
    """Answers questions related to CME's business and structure, e.g.
        regulations, compliance, CME's portfolio and offerings, etc. 
        Do not use this tool if you need access to a database or data 
        analytics to answer the question.
    """    

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=ClientOptions(api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com"))

    # The full resource name of the search app serving config
    serving_config = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{CME_WEBSITE_SEARCH_ENG_ID}/servingConfigs/default_config"

    # Optional: Configuration options for search
    # Refer to the `ContentSearchSpec` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest.ContentSearchSpec
    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        # For information about snippets, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/snippets
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        # For information about search summaries, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/get-search-summaries
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=5,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
            # model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
            #     preamble=''
            # ),
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version='stable',
            ),
        ),
    )

    # Refer to the `SearchRequest` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=question,
        page_size=10,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        ),
    )

    response = client.search(request)
    summary_and_citations = response.summary.summary_text

    for i in range(5):
        summary_and_citations += f'\n\n[{i+1}] '
        summary_and_citations += response.results[i].document.derived_struct_data.get('title') + '\n'
        summary_and_citations += response.results[i].document.derived_struct_data.get('link') + '\n'
        summary_and_citations += response.results[i].document.derived_struct_data.get('snippets')[0].get('snippet') + '\n'
    
    return summary_and_citations


def get_maestro_tools(user_role: str) -> list:

    match user_role:
        case UserRoles.SALESFORCE_USER_ROLE.value:
            # long-term: class setter method for available tables, update docstring
            return [fallback, cme_info_lookup, query_database, analyze_call_reports]
        case UserRoles.READONLY_USER_ROLE.value:
            # long-term: class setter method for available tables, update docstring
            return [fallback, cme_info_lookup, query_database]
        case _:
            raise ValueError(f'user role {user_role} is not currently supported.')
