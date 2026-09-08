import pytest
from bumpversion import __init__ as bumpversion_init

def test_known_vcs_mappings_non_git_mercurial():
    vcs_map = bumpversion_init.KNOWN_VCS
    assert 'hg' in vcs_map
    assert 'svn' in vcs_map

def test_vcs_map_content_types():
    vcs_map = bumpversion_init.KNOWN_VCS
    for key, value in vcs_map.items():
        assert isinstance(key, str)
        assert callable(value)

def test_default_vcs_scenarios():
    vcs_map = bumpversion_init.KNOWN_VCS
    # Must have git, use another well-known
    assert 'hg' in vcs_map or 'svn' in vcs_map