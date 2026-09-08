from src.ajpfuzzer.ajpfuzzer import AJPTestCases

def test_get_all_cases_non_empty():
    cases = AJPTestCases.get_all_cases()
    assert len(cases) > 0

def test_get_all_cases_contains_test():
    cases = AJPTestCases.get_all_cases()
    found = False
    for s in cases:
        if s.startswith("GET "):
            found = True
            break
    assert found