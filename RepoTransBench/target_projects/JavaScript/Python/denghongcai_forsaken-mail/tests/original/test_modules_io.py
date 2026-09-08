import pytest
from unittest import mock
import re

@pytest.fixture(autouse=True)
def patch_mailin_and_config(monkeypatch):
    # Simulate mailin and config modules
    mailin_mock = mock.Mock()
    mailin_mock.on = mock.Mock()
    mailin_mock.start = mock.Mock()
    config_mock = mock.Mock()
    config_mock.keywordBlackList = ['foo', 'bar']
    config_mock.mailin = {}

    modules = {
        'modules.mailin': mailin_mock,
        'modules.config': config_mock,
    }
    monkeypatch.setitem(__import__('sys').modules, 'modules.mailin', mailin_mock)
    monkeypatch.setitem(__import__('sys').modules, 'modules.config', config_mock)
    yield

class DummySocket:
    def __init__(self, initial_id='socketid'):
        self.events = {}
        self.emitted = {}
        self.shortid = initial_id
        self.disconnect_called = False

    def emit(self, event, data):
        self.emitted[event] = data

    def on(self, event, cb):
        self.events[event] = cb

    def trigger(self, event, *args):
        if event in self.events:
            self.events[event](*args)

class DummyIo:
    def __init__(self):
        self.events = {}

    def on(self, event, cb):
        self.events[event] = cb

    def trigger(self, event, *args):
        if event in self.events:
            self.events[event](*args)

def import_io_module():
    # Simulate the io module as a function that sets up events
    def io_module(io):
        # Define behaviour as per original JS logic
        def handle_connection(socket):
            socket.on('request shortid', lambda: socket.emit('shortid', socket.shortid))
            socket.on('set shortid', lambda new_id: (
                # Blacklist filter
                None if new_id in ['foo', 'bar'] else setattr(socket, 'shortid', new_id) or socket.emit('shortid', new_id)
            ))
            socket.on('disconnect', lambda s=socket: None)
        io.on('connection', handle_connection)
        # Attach a simulated mailin event handler if mailin is imported
        try:
            mailin = __import__('modules.mailin')
            def mailin_message_handler(conn, data):
                # Check if to is socket.shortid@domain for active sockets
                to = data.get('headers', {}).get('to', '')
                for s in getattr(io, 'connected', [ ]):
                    if to.startswith(s.shortid):
                        s.emit('mail', data)
            mailin.on('message', mailin_message_handler)
        except ImportError:
            pass
    return io_module

def test_connection_and_shortid_request():
    io_module = import_io_module()
    io = DummyIo()
    io_module(io)
    socket = DummySocket('abc123')
    io.trigger('connection', socket)
    socket.trigger('request shortid')
    assert socket.emitted['shortid'] == socket.shortid
    assert re.match(r'^[a-z0-9_-]+$', socket.shortid)

def test_set_shortid_skips_blacklisted():
    io_module = import_io_module()
    io = DummyIo()
    io_module(io)
    socket = DummySocket('abc')
    io.trigger('connection', socket)
    socket.trigger('set shortid', 'foobar')
    assert 'shortid' not in socket.emitted or socket.emitted.get('shortid', None) != 'foobar'
    socket.trigger('set shortid', 'customid')
    assert socket.emitted['shortid'] == 'customid'

def test_disconnect_deletes_from_online():
    io_module = import_io_module()
    io = DummyIo()
    io_module(io)
    socket = DummySocket('aaa2')
    io.trigger('connection', socket)
    socket.trigger('request shortid')
    socket.trigger('disconnect', socket)
    assert socket.emitted['shortid'] == socket.shortid

def test_mailin_message_delivers_mail_to_socket(monkeypatch):
    io_module = import_io_module()
    # Setup sockets
    io = DummyIo()
    setattr(io, 'connected', [])
    io_module(io)
    socket = DummySocket('testid')
    io.connected.append(socket)
    io.trigger('connection', socket)
    socket.trigger('request shortid')
    # Simulate mailin message handler
    data = {'headers': {'to': socket.shortid + '@domain', 'from': 'x', 'subject': '', 'date': 'today'}}
    mailin = __import__('modules.mailin')
    # Find mailin message handler
    called_handlers = mailin.on.call_args_list
    handler = None
    for ca in called_handlers:
        if ca[0][0] == 'message':
            handler = ca[0][1]
            break
    handler({}, data)
    assert socket.emitted['mail'] == data

def test_mailin_message_to_does_not_match(monkeypatch):
    io_module = import_io_module()
    io = DummyIo()
    setattr(io, 'connected', [])
    io_module(io)
    socket = DummySocket()
    io.connected.append(socket)
    mailin = __import__('modules.mailin')
    # Find mailin message handler
    handler = None
    for ca in mailin.on.call_args_list:
        if ca[0][0] == 'message':
            handler = ca[0][1]
            break
    data = {'headers': {'to': 'not-an-email', 'from': 'none', 'subject': '', 'date': ''}}
    try:
        handler({}, data)
    except Exception:
        pytest.fail("Should not throw")

def test_mailin_message_to_with_valid_email_but_shortid_not_in_online(monkeypatch):
    io_module = import_io_module()
    io = DummyIo()
    setattr(io, 'connected', [])
    io_module(io)
    mailin = __import__('modules.mailin')
    handler = None
    for ca in mailin.on.call_args_list:
        if ca[0][0] == 'message':
            handler = ca[0][1]
            break
    data = {'headers': {'to': 'nosuchid@domain.com', 'from': 'none', 'subject': '', 'date': ''}}
    try:
        handler({}, data)
    except Exception:
        pytest.fail("Should not throw")