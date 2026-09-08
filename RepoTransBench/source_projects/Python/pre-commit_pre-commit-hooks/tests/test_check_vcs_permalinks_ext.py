import tempfile
import os
import sys

import pytest

from pre_commit_hooks import check_vcs_permalinks

GITHUB_URL = b"https://github.com/foo/bar/blob/master/file.py#L2"
GITHUB_URL_BRANCH = b"https://github.com/foo/bar/blob/feature/file.py#L20"
GITHUB_URL_WITH_HASH = b"https://github.com/foo/bar/blob/09dcbc08/file.py#L1"
NONMATCH = b"https://notgithub.com/foo/bar/blob/master/file.py#L1"

def test_get_pattern_matches_expected():
    pattern = check_vcs_permalinks._get_pattern("github.com")
    # Good: branch link (should match)
    assert pattern.search(GITHUB_URL_BRANCH)
    # Bad: commit hash in url (shouldn't match)
    assert not pattern.search(GITHUB_URL_WITH_HASH)
    # Good: master branch
    assert pattern.search(GITHUB_URL)

def test_check_filename_detects(tmp_path, capsys):
    thefile = tmp_path / "testfile.txt"
    lines = [
        b"some stuff\n",
        GITHUB_URL+b"\n",
        NONMATCH+b"\n",
    ]
    thefile.write_bytes(b"".join(lines))
    patterns = [check_vcs_permalinks._get_pattern("github.com")]
    ret = check_vcs_permalinks._check_filename(str(thefile), patterns)
    assert ret == 1
    out = capsys.readouterr().out
    assert str(thefile) in out

def test_check_filename_no_hits(tmp_path, capsys):
    thefile = tmp_path / "testfile2.txt"
    thefile.write_bytes(b"Something else\n" + NONMATCH + b"\n")
    patterns = [check_vcs_permalinks._get_pattern("github.com")]
    ret = check_vcs_permalinks._check_filename(str(thefile), patterns)
    assert ret == 0
    out = capsys.readouterr().out
    assert "Non-permanent" not in out

def test_main_prints_warning(tmp_path, capsys):
    thefile = tmp_path / "foo.txt"
    thefile.write_bytes(GITHUB_URL+b"\n")
    with pytest.raises(SystemExit) as e:
        check_vcs_permalinks.main([str(thefile)])
    out = capsys.readouterr().out
    assert "Non-permanent github link detected" in out

def test_main_no_warn(tmp_path, capsys):
    thefile = tmp_path / "foo2.txt"
    thefile.write_bytes(NONMATCH+b"\n")
    ret = check_vcs_permalinks.main([str(thefile)])
    out = capsys.readouterr().out
    assert "Non-permanent" not in out
    assert ret == 0

def test_main_additional_github_domain(tmp_path, capsys):
    thefile = tmp_path / "foo3.txt"
    domain = "gh.acme.com"
    url = f"https://{domain}/u/b/blob/main/f.py#L99".encode()
    thefile.write_bytes(url+b"\n")
    with pytest.raises(SystemExit):
        check_vcs_permalinks.main([str(thefile), "--additional-github-domain", domain])
    out = capsys.readouterr().out
    assert "Non-permanent" in out