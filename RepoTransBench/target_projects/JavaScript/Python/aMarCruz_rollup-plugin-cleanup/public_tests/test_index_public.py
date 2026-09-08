import pytest
import os
import asyncio

from src.index import rollup_cleanup, CleanupError, get_fixture_path

@pytest.mark.asyncio
async def test_should_export_a_function_public():
    assert callable(rollup_cleanup)

@pytest.mark.asyncio
async def test_returns_expected_api_public():
    plugin = rollup_cleanup({'comments': 'license'})
    assert hasattr(plugin, 'name')
    assert hasattr(plugin, 'transform')

@pytest.mark.asyncio
async def test_runs_transform_and_cleans_up_custom_file_public():
    plugin = rollup_cleanup({})
    file = get_fixture_path('defaults.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert "eslint" not in result.code

@pytest.mark.asyncio
async def test_handles_invalid_code_with_different_error_file():
    plugin = rollup_cleanup({})
    file = get_fixture_path('issue_10.js')
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
async def test_ignores_files_not_matching_include_pattern():
    plugin = rollup_cleanup({'include': '**/*.bar'})
    file = get_fixture_path('defaults.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result is None

@pytest.mark.asyncio
async def test_includes_dotfoo_files_with_different_extension_config():
    plugin = rollup_cleanup({'extensions': ['.foo', '.bar']})
    file = get_fixture_path('extensions.foo')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result is not None
    assert "copyright" not in result.code

@pytest.mark.asyncio
async def test_removes_comments_with_a_different_regex():
    import re
    plugin = rollup_cleanup({'comments': re.compile('license', re.I)})
    file = get_fixture_path('comments.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert 'license' not in result.code.lower()

@pytest.mark.asyncio
async def test_removes_all_comments_from_long_comment_js_public():
    plugin = rollup_cleanup()
    file = get_fixture_path('long_comment.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert "TODO" not in result.code

@pytest.mark.asyncio
async def test_accepts_options_for_sourcemaps_public_diff():
    plugin = rollup_cleanup({'sourcemap': False})
    file = get_fixture_path('comments.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert result.map is None

@pytest.mark.asyncio
async def test_passes_with_ts_using_another_fixture():
    plugin = rollup_cleanup({'extensions': ['.js', '.ts']})
    file = get_fixture_path('ts3s.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert isinstance(result.code, str)

@pytest.mark.asyncio
async def test_does_not_modify_es7_syntax_public():
    plugin = rollup_cleanup({'preserveFirstComment': False})
    file = get_fixture_path('es7.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    result = await plugin.transform(code, file)
    assert isinstance(result.code, str)

@pytest.mark.asyncio
async def test_calls_this_error_for_different_error_public():
    called = {'v': False}
    class FakeThis:
        def error(self, err):
            called['v'] = True
            assert hasattr(err, 'position')
            raise err

    plugin = rollup_cleanup({})
    file = get_fixture_path('issue_11.js')
    with open(file, encoding='utf-8') as f:
        code = f.read()
    import contextlib
    with pytest.raises(CleanupError):
        try:
            await plugin.transform.__func__(plugin, code, file)
        except CleanupError as e:
            assert called['v'] is True
            raise