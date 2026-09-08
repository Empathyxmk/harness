import pytest

class CustomResource:
    def __init__(self, name):
        self.name = name
        self.status = "new"
    def use(self):
        self.status = f"{self.name} used"
    def destroy(self):
        self.status = "destroyed"

@pytest.fixture
def resource_public():
    res = CustomResource("RESOURCE_X_PUBLIC")
    yield res
    res.destroy()

def test_resource_name(resource_public):
    # Use a different name, check setup/usage logic
    assert resource_public.name == "RESOURCE_X_PUBLIC"
    resource_public.use()
    assert resource_public.status == "RESOURCE_X_PUBLIC used"

def test_resource_destroy(resource_public):
    resource_public.destroy()
    assert resource_public.status == "destroyed"