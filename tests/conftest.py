import pytest


@pytest.fixture
def sample_sources():
    return [
        {"id": "id-0", "title": "Alpha"},
        {"id": "id-1", "title": "Beta"},
    ]


@pytest.fixture
def title_to_id():
    return {"Alpha": "id-0", "Beta": "id-1"}