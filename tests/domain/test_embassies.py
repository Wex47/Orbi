from app.domain.embassies import get_israeli_embassies


def test_get_all_embassies():
    result = get_israeli_embassies()

    assert isinstance(result, list)
    if result:
        assert "country" in result[0]


def test_get_embassies_filtered_by_country():
    result = get_israeli_embassies(country="France")

    assert isinstance(result, list)
    for embassy in result:
        assert "France" in embassy.get("country", "")
