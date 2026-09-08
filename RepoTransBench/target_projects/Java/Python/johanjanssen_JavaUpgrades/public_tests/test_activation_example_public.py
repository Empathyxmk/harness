import pytest

class ActivationExample:
    def get_message(self):
        return "Activation completed, now activated!"

def test_get_message_public():
    example = ActivationExample()
    assert "activated" in example.get_message()