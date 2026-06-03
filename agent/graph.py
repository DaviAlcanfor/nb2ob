from functools import partial
from langgraph.graph import StateGraph, END

from agent.state import PipelineState
from agent.nodes.clusterizer import clusterizer_node
from agent.nodes.orchestrator import orchestrator_node
from agent.nodes.formatter import formatter_node
from config.settings import Config
from agent.llms import llm


config = Config()


def build_graph():
    """
    Builds and compiles the LangGraph pipeline.

    Returns:
        CompiledGraph: the compiled graph ready to be invoked
    """

    graph = StateGraph(PipelineState)

    graph.add_node("clusterizer",  partial(clusterizer_node,  llm=llm))
    graph.add_node("orchestrator", partial(orchestrator_node, llm=llm))
    graph.add_node("formatter",    partial(formatter_node,    llm=llm))

    graph.set_entry_point("clusterizer")

    graph.add_edge("clusterizer",  "orchestrator")
    graph.add_edge("orchestrator", "formatter")
    graph.add_edge("formatter",    END)

    return graph.compile()