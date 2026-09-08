from pywizlight import __version__

def test_public_version_format():
    # Check that it follows a common semver format but use a different assertion method
    version_numbers = __version__.split(".")
    assert len(version_numbers) == 3
    for num in version_numbers:
        assert num.isdigit()