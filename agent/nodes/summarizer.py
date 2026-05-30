from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser

from agent.prompts.summarizer import SummarizerPrompt
from agent.state import PipelineState


def summarizer_node(
    state: PipelineState,
    llm: BaseLanguageModel
) -> dict:
    """
    Creates a node for the summarizer agent

    Args:
        state (PipelineState): state with the current values of context
        llm (BaseLanguageModel): the language model for the agent

    Returns:
        dict: returns the updated keys from state
    """

    chain = SummarizerPrompt.get_prompt() | llm | StrOutputParser()

    summarized_sources = [
        {
            "id": source["id"],
            "title": source["title"],
            "summary": chain.invoke({"content": source["cleaned_content"]})
        }
        for source in state["cleaned_sources"]
    ]

    return {
        "summarized_sources": summarized_sources,
        "called_agents": ["summarizer"]
    }