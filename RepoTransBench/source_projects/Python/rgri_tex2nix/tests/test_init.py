import os
import io
import builtins
import types
import pytest

import tex2nix

def test_get_packages_basic():
    line = r"\usepackage{foo,bar}"
    pkgs = tex2nix.get_packages(line)
    assert "foo" in pkgs
    assert "bar" in pkgs

def test_get_packages_requirepackage():
    line = r"\RequirePackage{baz}"
    pkgs = tex2nix.get_packages(line)
    assert pkgs == {"baz"}

def test_get_packages_no_match():
    line = r"not a package line"
    pkgs = tex2nix.get_packages(line)
    assert pkgs == set()

def test_get_packages_whitespace():
    line = r"\usepackage{   foo ,   bar  }"
    pkgs = tex2nix.get_packages(line)
    assert pkgs == {"foo", "bar"}

def test_get_packages_empty_braces():
    line = r"\usepackage{}"
    pkgs = tex2nix.get_packages(line)
    # The regex group will be empty string, but split(',') == [''], so: set([''])
    # But actual code skips empty strings in the loop (arg.strip() == '' is added)
    # However, the implementation DOES add '' into the set
    assert pkgs == set()

def test_write_tex_env(tmp_path):
    pkgs = {"foo", "bar"}
    name = tex2nix.write_tex_env(str(tmp_path), pkgs)
    assert os.path.exists(name)
    with open(name, "r") as f:
        content = f.read()
        assert "foo" in content and "bar" in content

def test_collect_deps_calls(monkeypatch):
    called = {"_collect_deps": 0}
    def fake_collect(working_set, done, all_packages):
        while working_set:
            done.add(working_set.pop())
            called["_collect_deps"] += 1
    monkeypatch.setattr(tex2nix, '_collect_deps', fake_collect)
    pkgs = {"foo", "bar"}
    allpkgs = {"foo", "bar", "baz"}
    result = tex2nix.collect_deps(pkgs, allpkgs)
    assert "foo" in result and "bar" in result
    assert called["_collect_deps"] == 2

def test_extract_dependencies_and_collect(monkeypatch):
    pkgs_in = {r"\usepackage{a,b}", r"\usepackage{c}"}
    monkeypatch.setattr(tex2nix, "get_nix_packages", lambda: {"a", "b"})
    monkeypatch.setattr(tex2nix, "collect_deps", lambda x, y: set(x))
    lines = list(pkgs_in)
    result = tex2nix.extract_dependencies(lines)
    assert result == {"a", "b"}

def test_main_and_fileinput(monkeypatch, tmp_path):
    # Patch fileinput.input() to return lines, patch cwd, and others
    monkeypatch.setattr("fileinput.input", lambda: [r"\usepackage{ji,ki}", r"\RequirePackage{li}"])
    monkeypatch.setattr(tex2nix, "get_nix_packages", lambda: {"ji", "li"})
    monkeypatch.setattr(tex2nix, "collect_deps", lambda x, y: set(x))
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))
    outputs = {}
    def fake_write_tex_env(dir, pkgs):
        outputs["dir"] = dir
        outputs["pkgs"] = set(pkgs)
        return os.path.join(dir, "tex-env.nix")
    monkeypatch.setattr(tex2nix, "write_tex_env", fake_write_tex_env)
    tex2nix.main()
    assert outputs["dir"] == str(tmp_path)
    assert outputs["pkgs"] == {"ji", "li"}

def test__collect_deps_real(monkeypatch, tmp_path):
    # Cover _collect_deps, including file reading and package detection logic.
    # Setup a fake tex dir/file structure
    os.makedirs(tmp_path / "foo" / "tex", exist_ok=True)
    tex_file = tmp_path / "foo" / "tex" / "abc.sty"
    with open(tex_file, "w") as f:
        f.write(r"\usepackage{morepkg}\n")
    # monkeypatch subprocess.run for nix-build command
    class Result: pass
    def fake_run(cmd, check, text, stdout):
        r = Result()
        r.stdout = f"{tmp_path}/foo"
        return r
    monkeypatch.setattr("subprocess.run", fake_run)
    working_set = {"bar"}
    done = set()
    all_packages = {"morepkg", "bar"}
    # monkeypatch get_packages for underlying call in file content parsing
    monkeypatch.setattr(tex2nix, "get_packages", lambda l: {"morepkg"} if "morepkg" in l else set())
    tex2nix._collect_deps(working_set, done, all_packages)
    assert "bar" in done

def test_get_nix_packages_success(monkeypatch):
    # Covers get_nix_packages: parses subprocess output and json.loads.
    class R: pass
    expected = ["foo", "bar", "baz"]
    def fake_run(*a, **k):
        r = R()
        r.stdout = '["foo","bar","baz"]'
        return r
    monkeypatch.setattr("subprocess.run", fake_run)
    result = tex2nix.get_nix_packages()
    assert set(expected) == result

def test_write_tex_env_empty(tmp_path):
    # Edge case: No packages.
    pkgs = set()
    name = tex2nix.write_tex_env(str(tmp_path), pkgs)
    assert os.path.exists(name)
    with open(name, "r") as f:
        content = f.read()
        # Only header and footer
        assert "scheme-small" in content