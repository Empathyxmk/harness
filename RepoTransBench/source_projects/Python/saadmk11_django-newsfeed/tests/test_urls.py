import pytest
from django.urls import reverse, resolve
import newsfeed.urls

def test_urls_resolve_latest_issue():
    resolver = resolve('/newsfeed/')
    assert resolver.view_name == 'newsfeed:latest_issue'

def test_urls_resolve_issue_list():
    resolver = resolve('/newsfeed/issues/')
    assert resolver.view_name == 'newsfeed:issue_list'

def test_urls_resolve_issue_detail():
    resolver = resolve('/newsfeed/issues/test-issue/')
    assert resolver.view_name == 'newsfeed:issue_detail'

def test_urls_resolve_subscribe():
    resolver = resolve('/newsfeed/subscribe/')
    assert resolver.view_name == 'newsfeed:newsletter_subscribe'

def test_urls_resolve_subscription_confirm():
    import uuid
    token = uuid.uuid4()
    url = f'/newsfeed/subscribe/confirm/{token}/'
    resolver = resolve(url)
    assert resolver.view_name == 'newsfeed:newsletter_subscription_confirm'

def test_urls_resolve_unsubscribe():
    resolver = resolve('/newsfeed/unsubscribe/')
    assert resolver.view_name == 'newsfeed:newsletter_unsubscribe'