import pytest

class Profile:
    def __init__(self, context, name, email):
        self.name = name
        self.email = email
    def getName(self):
        return self.name
    def getEmail(self):
        return self.email

@pytest.fixture(scope="function")
def publicProfile():
    # Simulate Application context, just None for Python
    return Profile(None, "public_test_user", "public@email.com")

def test_profile_name_is_set_public(publicProfile):
    assert publicProfile.getName() == "public_test_user"

def test_profile_email_is_set_public(publicProfile):
    assert publicProfile.getEmail() == "public@email.com"