import pytest
from mammoth.styles import document_matchers

def test_matcher_tag_name_public():
    matcher = document_matchers.ParagraphMatcher(style_id="Heading3")
    para = type("Para", (), {"style_id": "Heading3"})
    assert matcher.matches(para)

def test_matcher_tag_name_negative_public():
    matcher = document_matchers.RunMatcher(style_id="StrongEmph")
    run = type("Run", (), {"style_id": "Emphatic"})
    assert not matcher.matches(run)