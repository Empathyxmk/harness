import pytest

class Profile:
    def __init__(self, context, name, email):
        self.name = name
        self.email = email
        self.phone = ""
    def setPhone(self, phone):
        self.phone = phone
    def getName(self):
        return self.name
    def getEmail(self):
        return self.email
    def getPhone(self):
        return self.phone

@pytest.fixture(scope="function")
def publicProfile():
    p = Profile(None, "public_name", "public@email.org")
    p.setPhone("123987456")
    return p

def test_name_public(publicProfile):
    assert publicProfile.getName() == "public_name"

def test_email_public(publicProfile):
    assert publicProfile.getEmail() == "public@email.org"

def test_phone_public(publicProfile):
    assert publicProfile.getPhone() == "123987456"