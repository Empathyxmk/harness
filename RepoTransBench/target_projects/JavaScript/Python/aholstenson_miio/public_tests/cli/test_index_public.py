import sys
import types
from unittest import mock
import os

def test_runs_yargs_commanddir_with_nondefault_folder(monkeypatch):
    yargs_mock = types.SimpleNamespace(
        commandDir=mock.Mock(),
        recommendCommands=mock.Mock(),
        demandCommand=mock.Mock(),
        argv={}
    )
    monkeypatch.setitem(sys.modules, 'yargs', yargs_mock)
    monkeypatch.setattr(os.path, "join", lambda *a: '/'.join(a))
    yargs_mock.commandDir('some/alternate/folder')
    yargs_mock.recommendCommands()
    yargs_mock.demandCommand()
    assert yargs_mock.commandDir.called
    assert yargs_mock.recommendCommands.called
    assert yargs_mock.demandCommand.called