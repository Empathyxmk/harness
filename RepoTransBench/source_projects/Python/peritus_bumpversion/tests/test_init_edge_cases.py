# Edge test: Only test existence of DESCRIPTION, which coverage and dir show is exported

def test_module_has_expected_minimal_exports():
    import bumpversion
    attrs = dir(bumpversion)
    # Should have DESCRIPTION
    assert "DESCRIPTION" in attrs