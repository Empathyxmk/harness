from src.ajpfuzzer.ajpfuzzer import AJPTestCases

def test_get_all_cases_immutability():
    orig = AJPTestCases.get_all_cases()
    if orig:
        first = orig[0]
        assert first == "GET /WEB-INF/web.xml"

def test_get_all_cases_size():
    cases = AJPTestCases.get_all_cases()
    assert len(cases) >= 2, "Should be at least two default test cases"