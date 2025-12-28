import pytest
from app.infrastructure import llm


@pytest.fixture(autouse=True)
def reset_llm_caches():
    """
    Ensure global caches are reset between tests.
    This prevents cross-test pollution.
    """
    llm._CHAT_MODEL_CACHE.clear()
    llm._LIGHTWEIGHT_MODEL_CACHE.clear()
    llm._VERIFIER_MODEL = None


def test_get_chat_model_caches_by_key(monkeypatch):
    created = []

    def fake_init_chat_model(*args, **kwargs):
        obj = object()
        created.append(obj)
        return obj

    monkeypatch.setattr(llm, "init_chat_model", fake_init_chat_model)

    m1 = llm.get_chat_model()
    m2 = llm.get_chat_model()

    assert m1 is m2
    assert len(created) == 1


def test_get_chat_model_different_temperature_creates_new(monkeypatch):
    created = []

    def fake_init_chat_model(*args, **kwargs):
        obj = object()
        created.append(obj)
        return obj

    monkeypatch.setattr(llm, "init_chat_model", fake_init_chat_model)

    m1 = llm.get_chat_model(temperature=0.1)
    m2 = llm.get_chat_model(temperature=0.2)

    assert m1 is not m2
    assert len(created) == 2


def test_get_chat_model_streaming_flag_affects_cache(monkeypatch):
    created = []

    def fake_init_chat_model(*args, **kwargs):
        obj = object()
        created.append(obj)
        return obj

    monkeypatch.setattr(llm, "init_chat_model", fake_init_chat_model)

    m1 = llm.get_chat_model(streaming=False)
    m2 = llm.get_chat_model(streaming=True)

    assert m1 is not m2
    assert len(created) == 2


def test_get_lightweight_chat_model_has_separate_cache(monkeypatch):
    created = []

    def fake_init_chat_model(*args, **kwargs):
        obj = object()
        created.append(obj)
        return obj

    monkeypatch.setattr(llm, "init_chat_model", fake_init_chat_model)

    m1 = llm.get_lightweight_chat_model()
    m2 = llm.get_lightweight_chat_model()

    assert m1 is m2
    assert len(created) == 1


def test_get_verifier_model_is_singleton(monkeypatch):
    created = []

    def fake_init_chat_model(*args, **kwargs):
        obj = object()
        created.append(obj)
        return obj

    monkeypatch.setattr(llm, "init_chat_model", fake_init_chat_model)

    v1 = llm.get_verifier_model()
    v2 = llm.get_verifier_model()

    assert v1 is v2
    assert len(created) == 1
