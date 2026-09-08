# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from adblockparser import AdblockRule

# Different comment rules than existing tests
COMMENT_RULES = [
    "! This is a comment line",
    "! Title: Example Filter List",
    "! Expires: 4 days",
    "! Homepage: https://example.com/",
    "[Adblock]",
    "!#include another_list.txt",
]

# Different HTML rules than existing tests
HTML_RULES = [
    "##.bannerAd",
    "@@##.sponsoredContent",
    "mysite.com#@##sidebar",
    "@@##.cookieBar",
    "example.net,example.org#@##promo",
    "##a[href^='https://tracker.example.com/']",
    '##img[src$=".ads.png"]',
]


@pytest.mark.parametrize("text", COMMENT_RULES)
def test_public_is_comment(text):
    rule = AdblockRule(text)
    assert rule.is_comment
    assert not rule.is_html_rule
    assert not rule.is_exception
    assert rule.options == {}
    assert not rule.regex


@pytest.mark.parametrize("text", HTML_RULES)
def test_public_is_html_rule(text):
    rule = AdblockRule(text)
    assert rule.is_html_rule
    assert not rule.is_comment