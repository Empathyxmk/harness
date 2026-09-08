import pytest

class DummyLog:
    indent = ''
    @staticmethod
    def info(*args):
        print(*args)
    @staticmethod
    def error(*args):
        print(*args)
    @staticmethod
    def warn(*args):
        print(*args)
    @staticmethod
    def plain(*args):
        print(*args)
    @staticmethod
    def group(func):
        prev = DummyLog.indent
        DummyLog.indent = '  '
        try:
            func()
        finally:
            DummyLog.indent = prev
    @staticmethod
    def device(info, extra=None):
        print('Device info:', info, extra)

@pytest.fixture(autouse=True)
def mock_print(monkeypatch):
    calls = []
    monkeypatch.setattr('builtins.print', lambda *a, **k: calls.append(a))
    yield calls

def test_log_info_with_different_words(mock_print):
    DummyLog.info('foo', 'bar', 'baz')
    assert mock_print

def test_log_error_with_alternate_message(mock_print):
    DummyLog.error('unexpected', 'problem')
    assert mock_print

def test_log_warn_with_alternate_text(mock_print):
    DummyLog.warn('alert', 'now')
    assert mock_print

def test_log_plain_with_alternate_values(mock_print):
    DummyLog.plain('simple', 'output')
    assert mock_print

def test_group_and_restore_indentation_public():
    orig_indent = DummyLog.indent
    def fn():
        DummyLog.warn('inside group')
        assert DummyLog.indent != orig_indent
    DummyLog.group(fn)
    assert DummyLog.indent == orig_indent

def test_print_device_info_all_public_branches(mock_print):
    DummyLog.device({
      "id": 'miio:654321',
      "metadata": { "types": set(['miio:type2', 'othertype2']), "capabilities": set(['x', 'y']) },
      "management": { "model": 'xyz', "address": 'otherip', "token": 'tok2', "autoToken": False }
    })
    DummyLog.device({
      "id": 'miio:888888',
      "metadata": { "types": set(['miio:type99']), "capabilities": set(['cap']) },
      "management": { "model": '', "address": 'otherip', "token": 'tok3', "autoToken": True }
    }, True)
    DummyLog.device({
      "id": 'miio:222222',
      "metadata": { "types": set(['typeX']), "capabilities": set(['c1']) },
      "management": { "model": 'modelX', "address": None, "parent": {"id":'parent1'}, "token": None }
    })
    DummyLog.device({
      "id": '54321',
      "metadata": { "types": set(['typeX']), "capabilities": set([]) },
      "management": { "model": None, "address": 'otherip', "parent": None, "token": None }
    })
    DummyLog.device({
      "id": 'miio:33333',
      "metadata": { "types": set(['miio:typeQ']), "capabilities": set(['q1']) },
      "management": { "model": 'mm', "address": None, "parent": {"id":'pp'}, "token": None }
    }, True)
    assert mock_print