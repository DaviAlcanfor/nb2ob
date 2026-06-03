from typing import List
from infrastructure.decorators import get_logger

from api._cleaning import _parse_summary_line


logger = get_logger(__name__)



_PROMPT_TEMPLATE = (
    "Summarize each of the following sources in exactly 2 sentences each.\n"
    "First sentence: the main topic. Second sentence: the key insight or conclusion.\n"
    "Respond ONLY in this exact format, one block per source, nothing else:\n\n"
    "[Source Title]: sentence 1. sentence 2.\n\n"
    "Sources to summarize:\n"
    "{source_list}"
)


def _build_summary_prompt(sources):
    
    title_to_id= {}
    titles = []
    
    for source in sources:
        title_to_id[source["title"]] = source["id"]
        titles.append(source["title"])
    
    source_list = "\n".join(titles)
    return title_to_id, _PROMPT_TEMPLATE.format(source_list=source_list)


def _parse_summaries(answer: str, title_to_id: dict) -> List:
    summaries = []
    
    for item in (_parse_summary_line(line) for line in answer.splitlines()):
    
        if item is None:
            continue
    
        title, summary = item
        source_id = title_to_id.get(title)
    
        if source_id is None:
            logger.warning(f"Unmatched title in summary response: {title!r}")
            continue
        summaries.append({"id": source_id, "title": title, "summary": summary})
    
    return summaries


