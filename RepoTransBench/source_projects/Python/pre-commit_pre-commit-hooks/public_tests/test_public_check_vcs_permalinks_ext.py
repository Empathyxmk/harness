import tempfile
import os
import sys

import pytest

from pre_commit_hooks import check_vcs_permalinks

BITBUCKET_URL = b"https://bitbucket.org/foo/bar/src/master/file.py#lines-5"
GITHUB_URL_NEWBRANCH = b"https://github.com/hello/world/blob/dev/file.py#L42"
GITHUB_URL_WITH_HASH2 = b"https://github.com/hello/world/blob/abc123de/file.py#L10"
NON_GITHUB_URL = b"https://gitlab.com/foo/bar/blob/master/file.py#L3"

def test_get_pattern_matches_other_branch():
    pattern = check_vcs_permalinks._get_pattern("github.com")
    # Good: new branch link (should match)
    assert pattern.search(GITHUB_URL_NEWBRANCH)
    # Bad: commit hash in url (shouldn't match)
    assert not pattern.search(GITHUB_URL_WITH_HASH2)
    # Bad: unrelated domain
    assert not pattern.search(BITBUCKET_URL)
    # Bad: unrelated domain
    assert not pattern.search(NON_GITHUB_URL)

def test_check_filename_detects_branch(tmp_path, capsys):
    thefile = tmp_path / "samplefile.txt"
    lines = [
        b"other stuff\n",
        GITHUB_URL_NEWBRANCH + b"\n",
        NON_GITHUB_URL + b"\n",
    ]
    thefile.write_bytes(b"".join(lines))
    patterns = [check_vcs_permalinks._get_pattern("github.com")]
    ret = check_vcs_permalinks._check_filename(str(thefile), patterns)
    assert ret == 1
    out = capsys.readouterr().out
    assert str(thefile) in out

def test_check_filename_no_github_hits(tmp_path, capsys):
    thefile = tmp_path / "samplefile2.txt"
    thefile.write_bytes(b"Nothing matches\n" + NON_GITHUB_URL + b"\n")
    patterns = [check_vcs_permalinks._get_pattern("github.com")]
    ret = check_vcs_permalinks._check_filename(str(thefile), patterns)
    assert ret == 0
    out = capsys.readouterr().out
    assert "Non-permanent" not in out

def test_main_prints_warning_with_branch(tmp_path, capsys):
    thefile = tmp_path / "testwarn.txt"
    thefile.write_bytes(GITHUB_URL_NEWBRANCH + b"\n")
    with pytest.raises(SystemExit):
        check_vcs_permalinks.main([str(thefile)])
    out = capsys.readouterr().out
    assert "Non-permanent github link detected" in out

def test_main_no_warn_with_gitlab(tmp_path, capsys):
    thefile = tmp_path / "testgitlab.txt"
    thefile.write_bytes(NON_GITHUB_URL + b"\n")
    ret = check_vcs_permalinks.main([str(thefile)])
    out = capsys.readouterr().out
    assert "Non-permanent" not in out
    assert ret == 0

def test_main_additional_other_github_domain(tmp_path, capsys):
    thefile = tmp_path / "customdomain.txt"
    domain = "git-hub.enterprise.com"
    url = f"https://{domain}/oscar/pre/blob/main/a.py#L48".encode()
    thefile.write_bytes(url + b"\n")
    with pytest.raises(SystemExit):
        check_vcs_permalinks.main([str(thefile), "--additional-github-domain", domain])
    out = capsys.readouterr().out
    assert "Non-permanent" in out