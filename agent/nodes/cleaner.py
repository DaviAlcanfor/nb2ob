from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser

from agent.prompts.cleaner import CleanerPrompt
from agent.state import PipelineState


def cleaner_node(
    state: PipelineState, 
    llm: BaseLanguageModel
) -> dict:
    """
    Creates a node for the cleaner agent

    Args:
        state (PipelineState): state with the current values of context
        llm (BaseLanguageModel): the language model for the agent 

    Returns:
        dict: returns the updated keys from state
    """
    
    chain = CleanerPrompt.get_prompt() | llm | StrOutputParser()

    sources = [
        source 
        for nb in state["notebooks"] 
        for source in nb["sources"]
    ]

    cleaned_sources = [
        {
            "id": source["id"],
            "title": source["title"],
            "cleaned_content": chain.invoke({"content": source["content"]})
        }
        for source in sources
    ]

    return {
        "cleaned_sources": cleaned_sources,
        "called_agents": ["cleaner"]
    }