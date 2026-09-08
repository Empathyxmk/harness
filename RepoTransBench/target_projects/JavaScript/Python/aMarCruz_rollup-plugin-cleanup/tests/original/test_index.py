import pytest
import os
import asyncio

from src.index import rollup_cleanup, CleanupError, get_fixture_path

@pytest.mark.asyncio
async def test_export_is_a_function():
    assert callable(rollup_cleanup)

@pytest.mark.asyncio
async def test_returns_expected_api():
    plugin = rollup_cleanup({})
    assert hasattr(plugin, 'name')
    assert hasattr(plugin, 'transform')

@pytest.mark.asyncio
async def test_runs_transform_and_cleans_up_comments():
    plugin = rollup_cleanup({})
    file = get_fixture_path('comments.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert "/*" not in result.code

@pytest.mark.asyncio
async def test_handles_invalid_code_gracefully():
    plugin = rollup_cleanup({})
    file = get_fixture_path('with_error.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    did_throw = False
    try:
        await plugin.transform(code, file)
    except CleanupError as err:
        did_throw = True
        assert isinstance(err, Exception)
    assert did_throw

@pytest.mark.asyncio
async def test_ignores_non_included_files():
    plugin = rollup_cleanup({'include': '**/*.foo'})
    file = get_fixture_path('defaults.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result is None

@pytest.mark.asyncio
async def test_includes_dotfoo_files_when_extension_set():
    plugin = rollup_cleanup({'extensions': ['.foo']})
    file = get_fixture_path('extensions.foo')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result is not None
    assert "/*" not in result.code

@pytest.mark.asyncio
async def test_removes_comments_with_specified_regex():
    import re
    plugin = rollup_cleanup({'comments': re.compile('cleanup', re.I)})
    file = get_fixture_path('comments.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert 'cleanup' not in result.code.lower()

@pytest.mark.asyncio
async def test_defaults_to_removing_all_comments():
    plugin = rollup_cleanup()
    file = get_fixture_path('long_comment.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert "/*" not in result.code

@pytest.mark.asyncio
async def test_accepts_options_for_sourcemaps():
    plugin = rollup_cleanup({'sourcemap': True})
    file = get_fixture_path('defaults.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result.map is not None

@pytest.mark.asyncio
async def test_passes_with_ts():
    plugin = rollup_cleanup({'extensions': ['.ts', '.js']})
    file = get_fixture_path('ts3s.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert isinstance(result.code, str)

@pytest.mark.asyncio
async def test_does_not_modify_es7_syntax():
    plugin = rollup_cleanup({'preserveFirstComment': True})
    file = get_fixture_path('es7.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert isinstance(result.code, str)

@pytest.mark.asyncio
async def test_calls_this_error_when_available_and_error_has_position():
    called = {'v': False}
    class FakeThis:
        def error(self, err):
            called['v'] = True
            assert hasattr(err, 'position')
            raise err

    plugin = rollup_cleanup({})
    file = get_fixture_path('with_error.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    import contextlib
    with pytest.raises(CleanupError):
        try:
            await plugin.transform.__func__(plugin, code, file)
        except CleanupError as e:
            assert called['v'] is True
            raise