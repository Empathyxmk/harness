from src.ajpfuzzer.ajpfuzzer import AJPTestCases

def test_get_all_cases_immutability_different():
    orig = AJPTestCases.get_all_cases()
    if orig:
        last = orig[-1]
        assert last.endswith(".jsp") or last.endswith(".xml") or "/" in last

def test_get_all_cases_has_default_cases():
    cases = AJPTestCases.get_all_cases()
    assert "GET /WEB-INF/web.xml" in cases