import pytest

@pytest.mark.skip(reason="Skipping due to missing ipware dependency required by pytracking.django.")
def test_skip_due_to_missing_ipware():
    pass