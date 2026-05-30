"""
Base class for all agent prompts.

Provides shared configuration and a generic get_prompt() method
that returns a ChatPromptTemplate ready to be used in a LangChain chain.
"""

from langchain_core.prompts import ChatPromptTemplate


class BasePrompt:
    OUTPUT_LANGUAGE: str = "English"
    SYSTEM_PROMPT: str = ""

    @classmethod
    def get_prompt(cls) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", cls.SYSTEM_PROMPT),
            ("human", "{content}")
        ])