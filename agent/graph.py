from functools import partial
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_cerebras import ChatCerebras
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from agent.state import PipelineState
from agent.nodes.cleaner import cleaner_node
from agent.nodes.summarizer import summarizer_node
from agent.nodes.clusterizer import clusterizer_node
from agent.nodes.orchestrator import orchestrator_node
from agent.nodes.formatter import formatter_node
from config.settings import Config
from config.models import BUILDERS, PROVIDER_MAP, API_KEYS, Model


config = Config()


def build_llm(
    temperature: float,
    top_p: Optional[float] = None,
    model: Optional[str] = None,
) -> ChatGoogleGenerativeAI | ChatGroq | ChatAnthropic | ChatCerebras | ChatOpenAI:
    """
    Builds an LLM instance based on the given model.
    top_p is only applied for Gemini models.
    base_url is only applied for OpenRouter models.
    """
    provider = PROVIDER_MAP.get(model)

    if provider is None:
        raise ValueError(f"Unknown model: {model}")

    kwargs = dict(
        model=model,
        temperature=temperature,
        api_key=API_KEYS.get(provider),
    )

    if top_p is not None and provider == "gemini":
        kwargs["top_p"] = top_p

    if provider == "openrouter":
        kwargs["base_url"] = config.openrouter_base_url

    return BUILDERS[provider](**kwargs)


def build_graph():
    """
    Builds and compiles the LangGraph pipeline.

    Returns:
        CompiledGraph: the compiled graph ready to be invoked
    """

    llm_principal = build_llm(model=Model.GEMINI_2_5_FLASH,   temperature=0.7, top_p=0.95)
    llm_fallback  = build_llm(model=Model.LLAMA_3_3_VERSATILE, temperature=0.7)
    llm_rapido    = build_llm(model=Model.LLAMA_3_3_CEREBRAS,  temperature=0.0)

    llm = llm_principal.with_fallbacks([llm_fallback, llm_rapido])

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