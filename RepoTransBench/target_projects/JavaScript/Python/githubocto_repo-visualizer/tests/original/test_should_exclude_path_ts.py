import pytest
from src.should_exclude_path import should_exclude_path

def test_excludes_based_on_folder_or_perfect_match_relative_to_root():
    exclude_paths = {'node_modules/', 'yarn.lock'}
    exclude_globs = []

    test = lambda path: should_exclude_path(path, exclude_paths, exclude_globs)
    assert test('node_modules/') is True
    assert test('yarn.lock') is True
    # Non-matched files work
    assert test('src/app.js') is False
    assert test('src/yarn.lock') is False

def test_excludes_based_on_micromatch_globs(monkeypatch):
    exclude_paths = set()
    exclude_globs = [
        'node_modules/**',
        '**/yarn.lock',
        '**/*.png',
        '**/!(*.module).ts'
    ]
    test = lambda path: should_exclude_path(path, exclude_paths, exclude_globs)

    monkeypatch.setattr("src.should_exclude_path.micromatch_is_match", lambda path, patterns: (
        path == 'node_modules/jest/index.js'
        or path == 'node_modules/jest'
        or path == 'yarn.lock'
        or path == 'subpackage/yarn.lock'
        or path in ['src/docs/boo.png', 'test/boo.png', 'boo.png']
        or (path == 'index.ts' and '**/!(*.module).ts' in patterns)
    ))
    assert test('node_modules/jest/index.js') is True
    assert test('node_modules/jest') is True
    assert test('yarn.lock') is True
    assert test('subpackage/yarn.lock') is True
    assert test('src/docs/boo.png') is True
    assert test('test/boo.png') is True
    assert test('boo.png') is True
    assert test('index.ts') is True
    assert test('index.module.ts') is False
    assert test('src/index.js') is False