import json

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from agent.prompts.clusterizer import ClusterizerPrompt
from agent.state import PipelineState


def clusterizer_node(
    state: PipelineState,
    llm: BaseLanguageModel
) -> dict:
    """
    Creates a node for the clusterizer agent

    Args:
        state (PipelineState): state with the current values of context
        llm (BaseLanguageModel): the language model for the agent

    Returns:
        dict: returns the updated keys from state
    """

    chain = ClusterizerPrompt.get_prompt() | llm | JsonOutputParser()

    sources_input = json.dumps(
        [
            {
                "id": source["id"], 
                "summary": source["summary"]
            }
            for source in state["summarized_sources"]
        ],
        ensure_ascii=False
    )

    clusters = chain.invoke({"content": sources_input})

    return {
        "clusters": clusters,
        "called_agents": ["clusterizer"]
    }