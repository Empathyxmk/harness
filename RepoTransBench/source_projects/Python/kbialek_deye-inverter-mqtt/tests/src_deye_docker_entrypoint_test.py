import unittest
import sys
import types
from unittest.mock import patch, MagicMock

# Patch out unavailable imports
sys.modules['deye_cli'] = types.SimpleNamespace(main=MagicMock())
sys.modules['deye_daemon'] = types.SimpleNamespace(main=MagicMock())
sys.modules['deye_config'] = types.SimpleNamespace(
    DeyeConfig=MagicMock(),
    LOG_DEST_STDOUT="stdout",
    LOG_DEST_STDERR="stderr",
)

import src.deye_docker_entrypoint as entrypoint


class DummyConfig:
    def __init__(self, log_stream, log_level="INFO"):
        self.log_stream = log_stream
        self.log_level = log_level


class TestDeyeDockerEntrypoint(unittest.TestCase):

    def test_setup_logging_stdout(self):
        cfg = DummyConfig("stdout", "INFO")
        with patch("src.deye_docker_entrypoint.logging.basicConfig") as m_basic:
            entrypoint.setupLogging(cfg)
            m_basic.assert_called()

    def test_setup_logging_stderr(self):
        cfg = DummyConfig("stderr", "DEBUG")
        with patch("src.deye_docker_entrypoint.logging.basicConfig") as m_basic:
            entrypoint.setupLogging(cfg)
            m_basic.assert_called()

    def test_setup_logging_invalid(self):
        cfg = DummyConfig("invalidstream")
        with self.assertRaises(ValueError):
            entrypoint.setupLogging(cfg)

    def test_main_cli(self):
        # Prepare mocks
        patch_config = patch("src.deye_docker_entrypoint.DeyeConfig.from_env", return_value=DummyConfig("stdout"))
        patch_setup = patch("src.deye_docker_entrypoint.setupLogging")
        patch_argv = patch.object(sys, "argv", ["dummy", "run"])
        patch_cli_main = patch("src.deye_docker_entrypoint.cli_main")
        patch_daemon_main = patch("src.deye_docker_entrypoint.daemon_main")

        with patch_config, patch_setup, patch_argv, patch_cli_main as m_cli, patch_daemon_main as m_daemon:
            entrypoint.main()
            m_cli.assert_called()
            m_daemon.assert_not_called()

    def test_main_daemon(self):
        patch_config = patch("src.deye_docker_entrypoint.DeyeConfig.from_env", return_value=DummyConfig("stdout"))
        patch_setup = patch("src.deye_docker_entrypoint.setupLogging")
        patch_argv = patch.object(sys, "argv", ["dummy"])
        patch_cli_main = patch("src.deye_docker_entrypoint.cli_main")
        patch_daemon_main = patch("src.deye_docker_entrypoint.daemon_main")

        with patch_config, patch_setup, patch_argv, patch_cli_main as m_cli, patch_daemon_main as m_daemon:
            entrypoint.main()
            m_cli.assert_not_called()
            m_daemon.assert_called()

    def test_main_config_exception(self):
        patch_config = patch("src.deye_docker_entrypoint.DeyeConfig.from_env", side_effect=Exception("fail"))
        patch_setup = patch("src.deye_docker_entrypoint.setupLogging")
        patch_stderr = patch("sys.stderr")
        patch_exit = patch("sys.exit")
        patch_argv = patch.object(sys, "argv", ["dummy"])
        with patch_config, patch_setup, patch_stderr, patch_exit as m_exit, patch_argv:
            entrypoint.main()
            m_exit.assert_called_with(1)


if __name__ == "__main__":
    unittest.main()