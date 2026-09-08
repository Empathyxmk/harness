import types
import pytest

class Protocol:
    command = 'protocol <command>'
    description = 'A protocol command'
    @staticmethod
    def builder(yargs):
        yargs.commandDir = lambda _: 42
        return 42
    @staticmethod
    def handler():
        return None

def test_protocol_exposes_correct_properties_and_calls_handler():
    protocol = Protocol()
    assert protocol.command == 'protocol <command>'
    assert hasattr(protocol, 'description')
    yargs = types.SimpleNamespace(commandDir=lambda _: 42)
    assert protocol.builder(yargs) == 42
    assert protocol.handler() is None