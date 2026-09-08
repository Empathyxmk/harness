import os
import sys
import importlib
import types
import builtins

import pytest

import graphios

def test_graphiosmetric_init():
    m = graphios.GraphiosMetric()
    assert isinstance(m, graphios.GraphiosMetric)

def test_main_prints_backend(tmp_path, monkeypatch):
    config_file = tmp_path / "graphios.cfg"
    config_file.write_text("[dummy]\nval=test\n")
    monkeypatch.setattr(sys, "argv", ["graphios.py", "--config_file", str(config_file), "--backend", "foobar"])
    monkeypatch.setattr("builtins.print", lambda x: None)
    monkeypatch.setattr("os.path.exists", lambda path: True)
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: output.append(" ".join(str(x) for x in a)))
    result = graphios.main()
    assert result == 0
    assert any("foobar" in o for o in output)

def test_main_missing_config(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["graphios.py", "--config_file", "notfound.cfg"])
    monkeypatch.setattr("os.path.exists", lambda path: False)
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: output.append(" ".join(str(x) for x in a)))
    monkeypatch.setattr(sys, "exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        graphios.main()
    assert any("modify the script" in o for o in output)

def test_parser_options_help():
    import subprocess
    import sys
    assert os.path.exists("graphios.py")
    result = subprocess.run([sys.executable, "graphios.py", "--help"], capture_output=True, text=True)
    assert "usage:" in result.stdout or "Options:" in result.stdout or result.returncode == 0

def test_logger_levels(capsys):
    log = graphios.Logger()
    log.debug("foo")
    log.info("bar")
    log.warn("qux")
    log.error("abc")
    log.critical("def")
    out = capsys.readouterr().out
    assert "[DEBUG]" in out
    assert "[INFO]" in out
    assert "[WARN]" in out
    assert "[ERROR]" in out
    assert "[CRITICAL]" in out

def test_logger_debug_env(monkeypatch, capsys):
    monkeypatch.setenv("GRAPHIOS_DEBUG", "1")
    import importlib
    import graphios as reload_graphios
    importlib.reload(reload_graphios)
    log = reload_graphios.Logger()
    log.debug("debug-print")
    assert "[DEBUG]" in capsys.readouterr().out

def test_logger_info(monkeypatch, capsys):
    log = graphios.Logger()
    log.info("Hello")
    assert "[INFO]" in capsys.readouterr().out

def test_graphiosmetric_repr_str():
    m = graphios.GraphiosMetric()
    assert isinstance(repr(m), str)
    assert isinstance(str(m), str)