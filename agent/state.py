from typing import TypedDict, Annotated
import operator
from typing import List

from api.notebooklm import Notebook, Sources


class Cluster(TypedDict):
    topic: str
    source_ids: list[str]


class FormattedNote(TypedDict):
    notebook_title: str 
    file_title: str
    content: str


class FilePlan(TypedDict):
    file_title: str
    source_ids: list[str]


class PipelineState(TypedDict):
    notebooks:          list[Notebook]
    clusters:           list[Cluster]
    file_plan:          list[FilePlan]
    formatted_notes:    list[FormattedNote]
    called_agents:      Annotated[list[str], operator.add]