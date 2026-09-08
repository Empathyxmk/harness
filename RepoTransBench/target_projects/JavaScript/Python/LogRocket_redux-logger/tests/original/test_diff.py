import pytest
from unittest import mock

def style(kind):
    return f"color for {kind}"

def render(diff_arg):
    kind = diff_arg.get('kind')
    path = diff_arg.get('path', [])
    if kind == 'E':
        return [*path, diff_arg.get('lhs'), '→', diff_arg.get('rhs')]
    if kind == 'N':
        return [*path, diff_arg.get('rhs')]
    if kind == 'D':
        return [*path]
    if kind == 'A':
        idx = diff_arg.get('index')
        item = diff_arg.get('item')
        return [f"{path[0]}[{idx}]", item] if path else []
    return []

def test_style_returns_correct_string():
    assert 'color' in style('E')
    assert 'color' in style('N')
    assert 'color' in style('D')
    assert 'color' in style('A')

def test_render_returns_correct_output_for_E():
    assert render({'kind': 'E', 'path': ['foo'], 'lhs': 1, 'rhs': 2}) == ['foo', 1, '→', 2]
def test_render_returns_correct_output_for_N():
    assert render({'kind': 'N', 'path': ['foo'], 'rhs': 2}) == ['foo', 2]
def test_render_returns_correct_output_for_D():
    assert render({'kind': 'D', 'path': ['bar']}) == ['bar']
def test_render_returns_correct_output_for_A():
    assert render({'kind': 'A', 'path': ['arr'], 'index': 1, 'item': 'baz'}) == ['arr[1]', 'baz']
def test_render_returns_empty_for_unknown():
    assert render({'kind': 'X'}) == []

def test_diffLogger_logs_groupCollapsed_when_isCollapsed():
    # fake "logger"
    logger = mock.Mock()
    logger.groupCollapsed = mock.Mock()
    logger.group = mock.Mock()
    logger.log = mock.Mock()
    logger.groupEnd = mock.Mock()
    # We'll fake deep-diff output as [{kind: 'E', path: ['foo'], lhs: 1, rhs: 2}]
    def fake_diff(prev, next, *_):
        return [{'kind': 'E', 'path': ['foo'], 'lhs': 1, 'rhs': 2}]
    # Simulating diffLogger
    prevState = {'foo': 1}
    newState = {'foo': 2}
    def diffLogger(prevState, newState, logger, isCollapsed):
        diffed = fake_diff(prevState, newState)
        if isCollapsed:
            logger.groupCollapsed('diff')
        else:
            logger.group('diff')
        for d in diffed:
            logger.log(str(render(d)))
        logger.groupEnd()
    diffLogger(prevState, newState, logger, True)
    logger.groupCollapsed.assert_called_with('diff')
    logger.log.assert_called()
    logger.groupEnd.assert_called()

def test_diffLogger_logs_group_when_not_isCollapsed():
    # fake "logger"
    logger = mock.Mock()
    logger.groupCollapsed = mock.Mock()
    logger.group = mock.Mock()
    logger.log = mock.Mock()
    logger.groupEnd = mock.Mock()
    def fake_diff(prev, next, *_):
        return [{'kind': 'N', 'path': ['foo'], 'rhs': 2}]
    prevState = {}
    newState = {'foo': 2}
    def diffLogger(prevState, newState, logger, isCollapsed):
        diffed = fake_diff(prevState, newState)
        if isCollapsed:
            logger.groupCollapsed('diff')
        else:
            logger.group('diff')
        for d in diffed:
            logger.log(str(render(d)))
        logger.groupEnd()
    diffLogger(prevState, newState, logger, False)
    logger.group.assert_called_with('diff')
    logger.log.assert_called()
    logger.groupEnd.assert_called()

def test_diffLogger_handles_no_diff():
    logger = mock.Mock()
    logger.groupCollapsed = mock.Mock()
    logger.group = mock.Mock()
    logger.log = mock.Mock()
    logger.groupEnd = mock.Mock()
    def fake_diff(prev, next, *_):
        return None
    def diffLogger(prevState, newState, logger, isCollapsed):
        diffed = fake_diff(prevState, newState)
        if not diffed:
            logger.log('—— no diff ——')
    diffLogger({}, {}, logger, False)
    logger.log.assert_called_with('—— no diff ——')