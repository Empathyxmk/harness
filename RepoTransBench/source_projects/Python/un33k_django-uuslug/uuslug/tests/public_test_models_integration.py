import pytest
from django.db import models
import sys

@pytest.mark.django_db
def test_cool_slug_model_save_public(monkeypatch):
    # Only run if testsettings module loaded
    if 'uuslug.models' not in sys.modules:
        import uuslug.models  # Triggers conditional model loading
    from uuslug.models import CoolSlug
    obj = CoolSlug(name="Awesome Python Tooling!")
    obj.save()
    assert "awesome-python-tooling" in obj.slug

@pytest.mark.django_db
def test_another_slug_model_save_public(monkeypatch):
    if 'uuslug.models' not in sys.modules:
        import uuslug.models
    from uuslug.models import AnotherSlug
    obj = AnotherSlug(name="Distinct Slug Value")
    obj.save()
    assert obj.slug.startswith("distinct-slug-value")

@pytest.mark.django_db
def test_truncated_slug_save_public(monkeypatch):
    if 'uuslug.models' not in sys.modules:
        import uuslug.models
    from uuslug.models import TruncatedSlug
    obj = TruncatedSlug(name="987 extra long truncated slug example")
    obj.save()
    assert len(obj.slug) <= 17