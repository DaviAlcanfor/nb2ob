import json

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser

from agent.prompts.formatter import FormatterPrompt
from agent.state import PipelineState


def formatter_node(
    state: PipelineState,
    llm: BaseLanguageModel
) -> dict:
    """
    Creates a node for the formatter agent

    Args:
        state (PipelineState): state with the current values of context
        llm (BaseLanguageModel): the language model for the agent

    Returns:
        dict: returns the updated keys from state
    """

    chain = FormatterPrompt.get_prompt() | llm | StrOutputParser()

    cleaned_by_id = {
        source["id"]: source
        for source in state["cleaned_sources"]
    }

    notebook_title = state["notebooks"][0]["title"]
    formatted_notes = [
        {
            "notebook_title": notebook_title,
            "file_title": file["file_title"],
            "content": chain.invoke({
                "content": json.dumps(
                    {   
                        "title": file["file_title"],
                        "sources": [
                            cleaned_by_id[sid]["cleaned_content"]
                            for sid in file["source_ids"]
                            if sid in cleaned_by_id
                        ]
                    },
                    ensure_ascii=False
                )
            })
        }
        for file in state["file_plan"]
    ]

    return {
        "formatted_notes": formatted_notes,
        "called_agents": ["formatter"]
    }