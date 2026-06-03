from typing import Optional

from config.models import BUILDERS, PROVIDER_MAP, API_KEYS, Model
from config.settings import Config

config = Config()


def build_llm(
    temperature: float,
    top_p: Optional[float] = None,
    model: Optional[str] = None,
):
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


llm_principal = build_llm(model=Model.LLAMA_3_3_VERSATILE, temperature=0.7)
llm_fallback  = build_llm(model=Model.LLAMA_3_3_CEREBRAS,  temperature=0.7)
llm_reserva   = build_llm(model=Model.DEEPSEEK_V3_FREE,     temperature=0.7)


llm = llm_principal.with_fallbacks([llm_fallback, llm_reserva])


__all__ = ["llm"]