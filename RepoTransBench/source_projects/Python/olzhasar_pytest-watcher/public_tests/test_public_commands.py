from pytest_watcher import commands
from pytest_watcher.config import Config
from pytest_watcher.terminal import Terminal
from pytest_watcher.trigger import Trigger

def test_run_alternate_command(trigger: Trigger, config: Config, mock_terminal: Terminal):
    class AnotherDummyCommand(commands.Command):
        character = "9"
        caption = "nine"
        description = "another test"
        show_in_menu = True

        def __init__(self):
            self.was_run = False

        def run(self, trigger: Trigger, term: Terminal, config: Config) -> None:
            self.was_run = True

    command = commands.Manager.get_command("9")

    assert isinstance(command, AnotherDummyCommand)
    assert command.was_run is False

    commands.Manager.run_command("9", trigger, mock_terminal, config)

    assert command.was_run is True

    commands.Manager._registry.pop(AnotherDummyCommand.character)