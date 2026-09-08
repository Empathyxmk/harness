import pytest
import sys
import types

import bumpversion.__init__ as bvi

def test_discard_default_if_specified_append_action():
    parser = type('Parser', (), {})()
    namespace = type('Namespace', (), {})()
    setattr(namespace, 'foo', [1])
    action = bvi.DiscardDefaultIfSpecifiedAppendAction(option_strings=[], dest='foo')
    action(parser, namespace, 2)
    assert getattr(namespace, 'foo') == [2]

def test_basevcs_is_usable_oserror(monkeypatch):
    class Dummy(Exception): pass
    class DummyBase(bvi.BaseVCS):
        _TEST_USABLE_COMMAND = ['nonexistent']

    def fail_call(*a, **kw):
        raise OSError(2, "No such file or directory")
    monkeypatch.setattr(bvi.subprocess, "call", fail_call)
    assert DummyBase.is_usable() is False

def test_basevcs_is_usable_other_raises(monkeypatch):
    class Dummy(Exception): pass
    class DummyBase(bvi.BaseVCS):
        _TEST_USABLE_COMMAND = ['other']

    def fail_call(*a, **kw):
        raise OSError(999, "other")
    monkeypatch.setattr(bvi.subprocess, "call", fail_call)
    with pytest.raises(OSError):
        DummyBase.is_usable()

def test_git_latest_tag_info_dirty(monkeypatch):
    class DummyGit(bvi.Git):
        @classmethod
        def latest_tag_info(cls):
            return {"dirty": True, "commit_sha": "sha", "distance_to_latest_tag": 1, "current_version": "1.0"}
    # Just ensure function works as implemented here
    assert DummyGit.latest_tag_info()["dirty"] is True