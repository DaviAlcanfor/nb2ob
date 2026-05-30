from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.language_models import BaseLanguageModel
from enum import Enum
from abc import ABC, abstractmethod


from agent.prompts import *
from agent.state import PipelineState


# TODO: Node class was prototyped but not implemented 
# node functions stay simpler and the abstraction adds overhead without enough 
# shared logic to justify it. 
# 
# Worth revisiting if cross-cutting concerns (retry, logging, error handling) 
# become non-trivial across nodes.



class Agent(Enum):
    def __init__(self, agent_name, prompt):
        self.agent_name = agent_name
        self.prompt = prompt
    
    CLEANER =      ("cleaner",      CleanerPrompt)
    CLUSTERIZER =  ("clusterizer",  ClusterizerPrompt)
    FORMATTER =    ("formatter",    FormatterPrompt)
    ORCHESTRATOR = ("orchestrator", OrchestratorPrompt)
    SUMMARIZER =   ("summarizer",   SummarizerPrompt)



class Node(ABC):
    def __init__(
        self,
        llm: BaseLanguageModel,
        agent: Agent,
        parser: StrOutputParser | JsonOutputParser,
    ):
        self.llm = llm
        self.agent_name = agent.agent_name
        self.chain = agent.prompt.get_prompt() | llm | parser


    def invoke(self, content):
        return self.chain.invoke({"content": content})


    @abstractmethod
    def __call__(self, state: PipelineState) -> dict:
        ...