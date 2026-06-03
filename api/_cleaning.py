import re

_GOOGLE_CDN_URL   = re.compile(r"https://lh3\.googleusercontent\.com\S+")
_IMAGE_TOKEN      = re.compile(r"\S+=w\d+-h\d+\S*")
_FLOATING_NEWLINE = re.compile(r"(?<!\n)\n(?!\n)")
_SUMMARY_LINE     = re.compile(r"^\[(.+?)\]:\s*(.+)$")


def _clean_content(content: str) -> str:
    content = _GOOGLE_CDN_URL.sub("", content)
    content = _IMAGE_TOKEN.sub("", content)
    content = _FLOATING_NEWLINE.sub(" ", content)
    
    return content.strip()


def _parse_summary_line(line: str) -> tuple[str, str] | None:
    m = _SUMMARY_LINE.match(line)
    return (m.group(1), m.group(2)) if m else None