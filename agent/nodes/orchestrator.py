import json

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from agent.prompts.orchestrator import OrchestratorPrompt
from agent.state import PipelineState


def orchestrator_node(
    state: PipelineState,
    llm: BaseLanguageModel
) -> dict:
    """
    Creates a node for the orchestrator agent

    Args:
        state (PipelineState): state with the current values of context
        llm (BaseLanguageModel): the language model for the agent

    Returns:
        dict: returns the updated keys from state
    """

    chain = OrchestratorPrompt.get_prompt() | llm | JsonOutputParser()

    clusters_input = json.dumps(
        state["clusters"], 
        ensure_ascii=False
    )

    file_plan = chain.invoke({"content": clusters_input})

    return {
        "file_plan": file_plan,
        "called_agents": ["orchestrator"]
    }