from src.vulhub.app import perform_attack

def contains_cas_lower_only(s):
    return s is not None and 'cas' in s

def test_contains_cas_substring_public():
    assert contains_cas_lower_only("this has cas inside")
    assert contains_cas_lower_only("xcasY")
    assert contains_cas_lower_only("casual")

def test_does_not_contain_cas_substring_public():
    assert not contains_cas_lower_only("CASE")
    assert not contains_cas_lower_only("archive")
    assert not contains_cas_lower_only("security")

def test_perform_attack_cas_present_public():
    target = "attackcas2024"
    expected = "Simulating CAS attack on attackcas2024"
    assert perform_attack(target) == expected

def test_perform_attack_cas_absent_public():
    target = "adminpanel"
    expected = "Target is not a CAS server: adminpanel"
    assert perform_attack(target) == expected

def test_perform_attack_only_cas_word_public():
    target = "CaS"
    expected = "Target is not a CAS server: CaS"
    assert perform_attack(target) == expected

def test_perform_attack_cas_in_middle_public():
    target = "alphaCasOmega"
    expected = "Target is not a CAS server: alphaCasOmega"
    assert perform_attack(target) == expected

def test_perform_attack_starts_with_cas_public():
    target = "casualty"
    expected = "Simulating CAS attack on casualty"
    assert perform_attack(target) == expected

def test_perform_attack_ends_with_cas_public():
    target = "smartsystems.cas"
    expected = "Simulating CAS attack on smartsystems.cas"
    assert perform_attack(target) == expected

def test_perform_attack_cas_like_but_not_cas_public():
    target = "CASE"
    expected = "Target is not a CAS server: CASE"
    assert perform_attack(target) == expected

def test_perform_attack_empty_string_public():
    target = ""
    expected = "Target is not a CAS server: "
    assert perform_attack(target) == expected