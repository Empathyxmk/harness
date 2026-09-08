import os
import io
import builtins
import pytest

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.xml')

def remove_access_example_com(config_path=CONFIG_FILE):
    try:
        with open(config_path, 'r', encoding='utf8') as f:
            config_data = f.read()
    except Exception as e:
        print('Error reading config.xml:', str(e))
        return
    # Remove the <access origin="example.com" /> line.
    import re
    config_data = re.sub(r'\s*<access origin="example\.com" \/>', '', config_data)
    try:
        with open(config_path, 'w', encoding='utf8') as f:
            f.write(config_data)
    except Exception as e:
        print('Error writing config.xml:', str(e))

def test_removes_access_example_com_from_config_xml(tmp_path, capsys):
    # Write a config.xml in tmp_path
    config_path = tmp_path / "config.xml"
    original_config = """
<widget>
    <access origin="https://first.com" />
    <access origin="example.com" />
    <access origin="https://last.com" />
</widget>
    """.strip()
    expected_config = """
<widget>
    <access origin="https://first.com" />
    <access origin="https://last.com" />
</widget>
    """.strip()
    config_path.write_text(original_config, encoding='utf8')
    # Perform the removal
    try:
        remove_access_example_com(str(config_path))
    except Exception:
        pass
    result = config_path.read_text(encoding='utf8')
    assert result == expected_config

def test_logs_error_if_readfile_fails_public_variant(tmp_path, capsys):
    config_path = tmp_path / "config.xml"
    # Remove file so readFile fails
    if config_path.exists():
        config_path.unlink()
    remove_access_example_com(str(config_path))
    captured = capsys.readouterr()
    assert "Error reading config.xml:" in captured.out

def test_logs_error_if_writefile_fails_public_variant(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "config.xml"
    config_path.write_text('<widget></widget>', encoding='utf8')
    orig_open = builtins.open
    def open_patch(file, mode='r', *args, **kwargs):
        if file == str(config_path) and 'w' in mode:
            raise Exception('Public simulated write error')
        return orig_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, 'open', open_patch)
    remove_access_example_com(str(config_path))
    captured = capsys.readouterr()
    assert "Error writing config.xml:" in captured.out and "Public simulated write error" in captured.out
    monkeypatch.setattr(builtins, 'open', orig_open)