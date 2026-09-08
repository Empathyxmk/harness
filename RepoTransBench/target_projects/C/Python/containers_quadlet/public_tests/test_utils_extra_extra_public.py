import pytest

def quad_replace_extension(filename, ext):
    if '.' in filename:
        core = '.'.join(filename.split('.')[:-1])
    else:
        core = filename
    return core + ext

def test_public_extra_extra():
    # Use a different string as per public version
    s = quad_replace_extension("archive.tar.tmp", ".complete")
    assert s == "archive.tar.complete"

    t = quad_replace_extension("config_public", ".conf")
    assert t == "config_public.conf"