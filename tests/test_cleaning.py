from api._cleaning import _clean_content, _remove_uuid_only_lines, _parse_summary_line


class TestRemoveUuidOnlyLines:
    def test_removes_line_with_only_uuid(self):
        content = "valid line\n550e8400-e29b-41d4-a716-446655440000\nanother line"
        result = _remove_uuid_only_lines(content)
        assert "550e8400" not in result
        assert "valid line" in result
        assert "another line" in result

    def test_keeps_line_with_uuid_and_text(self):
        content = "Source 550e8400-e29b-41d4-a716-446655440000 title"
        result = _remove_uuid_only_lines(content)
        assert "Source" in result
        assert "title" in result

    def test_removes_blank_lines(self):
        content = "line one\n   \nline two"
        result = _remove_uuid_only_lines(content)
        assert "   " not in result

    def test_empty_string_returns_empty(self):
        assert _remove_uuid_only_lines("") == ""


class TestCleanContent:
    def test_removes_google_cdn_url(self):
        content = "See https://lh3.googleusercontent.com/abc123xyz for details"
        result = _clean_content(content)
        assert "lh3.googleusercontent.com" not in result
        assert "See" in result

    def test_removes_image_token(self):
        content = "Image token: abc=w400-h300-rj present here"
        result = _clean_content(content)
        assert "=w400-h300" not in result

    def test_removes_uuid(self):
        content = "ID: 550e8400-e29b-41d4-a716-446655440000 end"
        result = _clean_content(content)
        assert "550e8400" not in result

    def test_joins_floating_newlines(self):
        content = "first line\nsecond line"
        result = _clean_content(content)
        assert result == "first line second line"

    def test_preserves_double_newlines(self):
        content = "paragraph one\n\nparagraph two"
        result = _clean_content(content)
        assert "\n\n" in result

    def test_strips_surrounding_whitespace(self):
        assert _clean_content("  clean content  ") == "clean content"

    def test_empty_string_returns_empty(self):
        assert _clean_content("") == ""


class TestParseSummaryLine:
    def test_parses_valid_line(self):
        line = "[My Source]: This is the summary text."
        assert _parse_summary_line(line) == ("My Source", "This is the summary text.")

    def test_returns_none_for_invalid_line(self):
        assert _parse_summary_line("No brackets here") is None

    def test_returns_none_for_empty_string(self):
        assert _parse_summary_line("") is None

    def test_parses_title_with_spaces(self):
        title, _ = _parse_summary_line("[Title With Spaces]: Summary sentence.")
        assert title == "Title With Spaces"

    def test_parses_summary_with_colon(self):
        _, summary = _parse_summary_line("[Source]: Key insight: something important.")
        assert summary == "Key insight: something important."