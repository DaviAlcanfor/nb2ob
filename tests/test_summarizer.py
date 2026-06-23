import pytest

from api._summarizer import _build_summary_prompt, _parse_summaries


class TestBuildSummaryPrompt:
    def test_returns_correct_title_to_id_mapping(self, sample_sources):
        title_to_id, _ = _build_summary_prompt(sample_sources)
        assert title_to_id == {"Alpha": "id-0", "Beta": "id-1"}

    def test_prompt_contains_all_titles(self, sample_sources):
        _, prompt = _build_summary_prompt(sample_sources)
        assert "Alpha" in prompt
        assert "Beta" in prompt

    def test_empty_sources_returns_empty_mapping(self):
        title_to_id, prompt = _build_summary_prompt([])
        assert title_to_id == {}
        assert "Sources to summarize:" in prompt

    def test_single_source(self):
        sources = [{"id": "id-0", "title": "Only One"}]
        title_to_id, prompt = _build_summary_prompt(sources)
        assert "Only One" in title_to_id
        assert "Only One" in prompt


class TestParseSummaries:
    def test_parses_single_valid_line(self, title_to_id):
        answer = "[Alpha]: First sentence. Second sentence."
        result = _parse_summaries(answer, title_to_id)
        assert len(result) == 1
        assert result[0] == {
            "id": "id-0",
            "title": "Alpha",
            "summary": "First sentence. Second sentence.",
        }

    def test_parses_multiple_valid_lines(self, title_to_id):
        answer = "[Alpha]: Summary A.\n[Beta]: Summary B."
        result = _parse_summaries(answer, title_to_id)
        assert len(result) == 2

    def test_skips_unmatched_title(self, title_to_id):
        answer = "[Unknown]: Some summary."
        result = _parse_summaries(answer, title_to_id)
        assert result == []

    def test_skips_blank_lines(self, title_to_id):
        answer = "[Alpha]: Summary.\n\n[Beta]: Another."
        result = _parse_summaries(answer, title_to_id)
        assert len(result) == 2

    def test_empty_answer_returns_empty_list(self, title_to_id):
        assert _parse_summaries("", title_to_id) == []

    def test_output_keys_are_correct(self):
        answer = "[Alpha]: The summary text."
        result = _parse_summaries(answer, {"Alpha": "abc-123"})
        assert set(result[0].keys()) == {"id", "title", "summary"}