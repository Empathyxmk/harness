import pytest

from honcho import command


@pytest.mark.parametrize('commands', [
    [
        ['start', '-p', '8080'],
        ['-p', '8080', 'start'],
    ],
    [
        ['start', '--procfile', 'Customfile'],
        ['--procfile', 'Customfile', 'start'],
    ],
    [
        ['start', '--no-prefix'],
        ['--no-prefix', 'start'],
    ],
    [
        ['start', '--no-colour', '--no-prefix'],
        ['--no-prefix', '--no-colour', 'start'],
        ['--no-colour', 'start', '--no-prefix'],
    ]
])
def test_command_equivalence_public(commands):
    if len(commands) < 2:
        pytest.fail("Must supply at least two commands")

    reference_args = commands.pop(0)
    reference_result = command.parser.parse_args(reference_args)

    for args in commands:
        result = command.parser.parse_args(args)
        assert result == reference_result


def test_port_precedence_public(monkeypatch):
    # Nothing specified -- should return default
    args = command.parser.parse_args(['start'])
    result = command.map_from(args)['port']
    assert result == '5000'

    # OS environment override (different value)
    monkeypatch.setenv('PORT', '6500')
    result = command.map_from(args)['port']
    assert result == '6500'

    # App environment override (different value)
    def _read_env(app_root, env):
        return {'PORT': '6700'}
    monkeypatch.setattr(command, '_read_env', _read_env)
    args = command.parser.parse_args(['start'])
    result = command.map_from(args)['port']
    assert result == '6700'

    # CLI override (different value)
    args = command.parser.parse_args(['start', '-p', '8800'])
    result = command.map_from(args)['port']
    assert result == '8800'


def test_procfile_precedence_public(monkeypatch):
    # Nothing specified -- should return default
    args = command.parser.parse_args(['start'])
    result = command.map_from(args)['procfile']
    assert result == 'Procfile'

    # OS environment override (different)
    monkeypatch.setenv('PROCFILE', 'CustomProcfile.env')
    result = command.map_from(args)['procfile']
    assert result == 'CustomProcfile.env'

    # App environment override (different)
    def _read_env(app_root, env):
        return {'PROCFILE': 'CustomProcfile.app'}
    monkeypatch.setattr(command, '_read_env', _read_env)
    args = command.parser.parse_args(['start'])
    result = command.map_from(args)['procfile']
    assert result == 'CustomProcfile.app'

    # CLI override (different)
    args = command.parser.parse_args(['start', '-f', 'CustomProcfile.cli'])
    result = command.map_from(args)['procfile']
    assert result == 'CustomProcfile.cli'