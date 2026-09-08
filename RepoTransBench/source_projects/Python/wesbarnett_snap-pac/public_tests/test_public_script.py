import tempfile
from pathlib import Path
import os

import pytest

from scripts.snap_pac import check_skip, ConfigProcessor, get_snapper_configs, Prefile, SnapperCmd


@pytest.mark.parametrize("snapper_cmd, actual_cmd", [
    (
        SnapperCmd("data", "pre", "timeline", "baz"),
        "snapper --config data create --cleanup-algorithm timeline --print-number --description \"baz\" --type pre"
    ),
    (
        SnapperCmd("home", "post", "timeline", "qux", False, 4321),
        "snapper --config home create --cleanup-algorithm timeline --print-number"
        " --description \"qux\" --pre-number 4321 --type post"
    ),
    (
        SnapperCmd("data", "post", "timeline", "quux", True, 5678),
        "snapper --no-dbus --config data create --cleanup-algorithm timeline --print-number"
        " --description \"quux\" --pre-number 5678 --type post"
    ),
    (
        SnapperCmd("foo", "post", "timeline", "snap", False, 8765, "bar=foo"),
        "snapper --config foo create --cleanup-algorithm timeline --print-number"
        " --description \"snap\" --userdata \"bar=foo\" --pre-number 8765 --type post"
    ),
    (
        SnapperCmd("home", "post", "timeline", "test", False, 2468, "alpha=beta,gamma=delta"),
        "snapper --config home create --cleanup-algorithm timeline --print-number"
        " --description \"test\" --userdata \"alpha=beta,gamma=delta\" --pre-number 2468 --type post"
    ),
    (
        SnapperCmd("data", "post", "timeline", "snap", False, None, "foo=bar,baz=qux"),
        "snapper --config data create --cleanup-algorithm timeline --print-number"
        " --description \"snap\" --userdata \"foo=bar,baz=qux\" --type single"
    )
])
def test_public_snapper_cmd(snapper_cmd, actual_cmd):
    assert str(snapper_cmd) == actual_cmd


def test_public_get_snapper_configs():
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("## Path: System/Snapper\n")
        f.write("\n")
        f.write("## Type:        string\n")
        f.write("## Default:     \"\"\n")
        f.write("# List of snapper configurations.\n")
        f.write("SNAPPER_CONFIGS=\"data home alpha beta\"\n")
        name = f.name
    assert get_snapper_configs(Path(name)) == ["data", "home", "alpha", "beta"]


def test_public_skip_snap_pac():
    os.environ["SNAP_PAC_SKIP"] = "yes"
    assert check_skip() is True


@pytest.mark.parametrize("section, command, packages, snapshot_type, result", [
    (
        "home", "bar", ["qux"], "pre",
        {"description": "bar", "cleanup_algorithm": "timeline", "userdata": "", "snapshot": True}
    ),
    (
        "data", "apt-get update", [], "pre",
        {"description": "apt-get update", "cleanup_algorithm": "timeline", "userdata": "critical=yes", "snapshot": True}
    ),
    (
        "archive", "apt-get update", [], "pre",
        {"description": "apt-get update", "cleanup_algorithm": "timeline", "userdata": "", "snapshot": False}
    ),
    (
        "beta", "apt-get update", [], "pre",
        {"description": "apt", "cleanup_algorithm": "timeline", "userdata": "foo=bar,requestid=99", "snapshot": True}
    ),
    (
        "beta", "apt-get update", [], "post",
        {"description": "test d", "cleanup_algorithm": "timeline", "userdata": "foo=bar,requestid=99", "snapshot": True}
    ),
    (
        "special", "apt-get install kernel", ["kernel"], "post",
        {"description": "kernel", "cleanup_algorithm": "number",
         "userdata": "foo=bar,critical=yes,requestid=99", "snapshot": True}
    ),
])
def test_public_config_processor(section, command, packages, snapshot_type, result):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("[home]\n")
        f.write("important_commands = [\"apt-get update\"]\n\n")
        f.write("cleanup_algorithm = timeline\n")
        f.write("[beta]\n")
        f.write("snapshot = True\n")
        f.write("desc_limit = 5\n")
        f.write("post_description = test description for beta section\n")
        f.write("userdata = [\"foo=bar\", \"requestid=99\"]\n\n")
        f.write("[special]\n")
        f.write("snapshot = True\n")
        f.write("cleanup_algorithm = number\n")
        f.write("important_packages = [\"kernel\", \"initrd\"]\n")
        f.write("userdata = [\"foo=bar\", \"requestid=99\"]\n")
        name = f.name
    config_processor = ConfigProcessor(name, snapshot_type, command, packages)
    assert config_processor(section) == result


def test_public_prefile_read_none():
    prefile = Prefile("data", "pre")
    assert prefile.read() is None


def test_public_prefile_read():
    prefile = Prefile("home", "pre")
    prefile.write("5678")
    prefile = Prefile("home", "post")
    assert prefile.read() == "5678"


def test_public_no_prefile():
    prefile = Prefile("nonexistent-pre-file", "post")
    assert prefile.read() is None