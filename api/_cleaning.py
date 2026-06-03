import re

_GOOGLE_CDN_URL   = re.compile(r"https://lh3\.googleusercontent\.com\S+")
_IMAGE_TOKEN      = re.compile(r"\S+=w\d+-h\d+\S*")
_FLOATING_NEWLINE = re.compile(r"(?<!\n)\n(?!\n)")
_SUMMARY_LINE     = re.compile(r"^\[(.+?)\]:\s*(.+)$")
_UUID             = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
_BLANK_LINE       = re.compile(r"^\s*$", re.MULTILINE)


def _remove_uuid_only_lines(content: str) -> str:
    lines = content.splitlines()
    cleaned = [line for line in lines if not _BLANK_LINE.match(_UUID.sub("", line))]
    return "\n".join(cleaned)


def _clean_content(content: str) -> str:
    content = _GOOGLE_CDN_URL.sub("", content)
    content = _IMAGE_TOKEN.sub("", content)
    content = _UUID.sub("", content)
    content = _remove_uuid_only_lines(content)
    content = _FLOATING_NEWLINE.sub(" ", content)

    return content.strip()


def _parse_summary_line(line: str) -> tuple[str, str] | None:
    m = _SUMMARY_LINE.match(line)
    return (m.group(1), m.group(2)) if m else None