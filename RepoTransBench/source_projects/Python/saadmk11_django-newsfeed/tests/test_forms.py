import pytest
from newsfeed.forms import SubscriberEmailForm

@pytest.mark.django_db
def test_valid_email():
    data = {'email_address': 'test@example.com'}
    form = SubscriberEmailForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data['email_address'] == 'test@example.com'

@pytest.mark.django_db
def test_invalid_email():
    data = {'email_address': 'not-an-email'}
    form = SubscriberEmailForm(data=data)
    assert not form.is_valid()
    assert 'email_address' in form.errors

@pytest.mark.django_db
def test_missing_email():
    form = SubscriberEmailForm(data={})
    assert not form.is_valid()
    assert 'email_address' in form.errors