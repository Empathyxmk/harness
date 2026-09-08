import sys
import os
import pytest
from src.hyeonwoonoh_deconvnet.inference.startup import startup

class TestStartup:
    def test_paths_added(self, tmp_path, monkeypatch):
        prev_sys_path = list(sys.path)
        # Run
        startup()
        assert any('inference/ext/densecrf' in p or 'inference/util' in p or 'inference' in p for p in sys.path)
        sys.path = prev_sys_path

    def test_clear_commands(self):
        # Nothing to clear in Python, just ensure function exists and does nothing
        assert startup()