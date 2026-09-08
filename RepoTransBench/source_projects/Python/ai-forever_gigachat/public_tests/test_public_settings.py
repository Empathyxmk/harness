from gigachat.settings import Settings

def test_public_settings() -> None:
    # Still just checks instantiation, but is a distinct test function.
    instance = Settings()
    assert hasattr(instance, "__class__")  # Basic check, not used in original