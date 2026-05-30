from functools import partial

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from agent.state import PipelineState
from agent.nodes.cleaner import cleaner_node
from agent.nodes.summarizer import summarizer_node
from agent.nodes.clusterizer import clusterizer_node
from agent.nodes.orchestrator import orchestrator_node
from agent.nodes.formatter import formatter_node
from config.settings import Config
from config.models import Model


def build_graph():
    """
    Builds and compiles the LangGraph pipeline.

    Returns:
        CompiledGraph: the compiled graph ready to be invoked
    """

    config = Config()

    llm = ChatGroq(model=Model.LLAMA_3_3_VERSATILE, api_key=config.groq_api_key)
    # other llms

    graph = StateGraph(PipelineState)

    graph.add_node("cleaner",      partial(cleaner_node,      llm=llm))
    graph.add_node("summarizer",   partial(summarizer_node,   llm=llm))
    graph.add_node("clusterizer",  partial(clusterizer_node,  llm=llm))
    graph.add_node("orchestrator", partial(orchestrator_node, llm=llm))
    graph.add_node("formatter",    partial(formatter_node,    llm=llm))

    graph.set_entry_point("cleaner")

    graph.add_edge("cleaner",      "summarizer")
    graph.add_edge("summarizer",   "clusterizer")
    graph.add_edge("clusterizer",  "orchestrator")
    graph.add_edge("orchestrator", "formatter")
    graph.add_edge("formatter",    END)

    return graph.compile()