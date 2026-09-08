import pytest
from src.ajpfuzzer.ajpfuzzer import AJPTestCases

def test_get_all_cases_returns_non_empty_list():
    cases = AJPTestCases.get_all_cases()
    assert cases is not None
    assert len(cases) > 0

def test_case_contains_known_attack_payloads():
    cases = AJPTestCases.get_all_cases()
    found = None
    for s in cases:
        if "/WEB-INF/web.xml" in s:
            found = s
            break
    assert found is not None

def test_list_is_unmodifiable():
    c1 = AJPTestCases.get_all_cases()
    # Tuple returned from get_all_cases is immutable; attempt to append must fail
    with pytest.raises((AttributeError, TypeError)):
        c1.append("test-case")