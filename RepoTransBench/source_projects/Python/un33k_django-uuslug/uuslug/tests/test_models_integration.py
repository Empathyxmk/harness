import pytest
from django.db import models
import sys

@pytest.mark.django_db
def test_cool_slug_model_save(monkeypatch):
    # Only run if testsettings module loaded
    if 'uuslug.models' not in sys.modules:
        import uuslug.models  # Triggers conditional model loading
    from uuslug.models import CoolSlug
    obj = CoolSlug(name="Django Is Great!")
    obj.save()
    assert "django-is-great" in obj.slug

@pytest.mark.django_db
def test_another_slug_model_save(monkeypatch):
    if 'uuslug.models' not in sys.modules:
        import uuslug.models
    from uuslug.models import AnotherSlug
    obj = AnotherSlug(name="Unique Name For Slug")
    obj.save()
    assert obj.slug.startswith("unique-name-for-slug")

@pytest.mark.django_db
def test_truncated_slug_save(monkeypatch):
    if 'uuslug.models' not in sys.modules:
        import uuslug.models
    from uuslug.models import TruncatedSlug
    obj = TruncatedSlug(name="321 short truncate slug name")
    obj.save()
    assert len(obj.slug) <= 17