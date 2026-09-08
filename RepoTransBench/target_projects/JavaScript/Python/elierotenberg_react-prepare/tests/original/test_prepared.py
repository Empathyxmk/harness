import pytest
from unittest.mock import MagicMock
from deepdiff import DeepDiff

# Simulating prepared logic
def deep_equal(a, b):
    return not DeepDiff(a, b, ignore_order=True)

def is_prepared(obj):
    # Only for simulation; real test would wrap/uncover metadata.
    return hasattr(obj, '_is_prepared') and obj._is_prepared

def get_prepare(obj):
    return getattr(obj, '_prepare', None)

def prepared(prepare_fn, options=None):
    def decorator(component):
        class PreparedWrapper:
            _is_prepared = True
            _prepare = staticmethod(prepare_fn)
            def __init__(self, *args, **kwargs):
                self.component = component
                self.props = kwargs
            def render(self):
                return component(**self.props)
        return PreparedWrapper
    return decorator

def test_prepared_composite_component():
    async def doAsyncSideEffect(text): pass
    doAsyncSideEffect_spy = MagicMock(side_effect=doAsyncSideEffect)

    async def prepareUsingProps(props):
        await doAsyncSideEffect_spy(props['text'])

    prepareUsingProps_spy = MagicMock(side_effect=prepareUsingProps)

    class OriginalCompositeComponent:
        def __init__(self, text):
            self.text = text
        def __call__(self, **kwargs):
            return f"<div>{kwargs['text']}</div>"

    class PreparedCompositeComponent(
        prepared(prepareUsingProps_spy, {'pure': False})(OriginalCompositeComponent)
    ):
        pass

    # Simulate unprepared
    class PlainComponent: pass

    assert not is_prepared(PlainComponent), "OriginalComponent is not prepared"
    assert is_prepared(PreparedCompositeComponent), "PreparedComponent is prepared"

    prepare = get_prepare(PreparedCompositeComponent)
    assert callable(prepare), "getPrepare(PreparedCompositeComponent) is a function"
    import asyncio
    asyncio.run(prepare({'text': 'foo'}))

    assert prepareUsingProps_spy.call_count == 1, "prepareUsingProps called once"
    called_args = prepareUsingProps_spy.call_args[0][0]
    assert deep_equal(called_args, {'text': 'foo'}), "prepareUsingProps called with correct args"
    assert doAsyncSideEffect_spy.call_count == 1, "doAsyncSideEffect called exactly once"
    do_sideeffect_args = doAsyncSideEffect_spy.call_args[0][0]
    assert do_sideeffect_args == 'foo', "doAsyncSideEffect called with correct argument"

    rendered = PreparedCompositeComponent(text='foo').render()
    assert rendered == "<div>foo</div>", "renders with correct html"

def test_prepared_composite_pure_component():
    async def doAsyncSideEffect(text): pass
    doAsyncSideEffect_spy = MagicMock(side_effect=doAsyncSideEffect)

    async def prepareUsingProps(props):
        await doAsyncSideEffect_spy(props['text'])

    prepareUsingProps_spy = MagicMock(side_effect=prepareUsingProps)

    class OriginalCompositePureComponent:
        def __init__(self, text):
            self.text = text
        def __call__(self, **kwargs):
            return f"<div>{kwargs['text']}</div>"

    class PreparedCompositeComponent(
        prepared(prepareUsingProps_spy)(OriginalCompositePureComponent)
    ):
        pass

    class PlainComponent: pass

    assert not is_prepared(PlainComponent), "OriginalComponent is not prepared"
    assert is_prepared(PreparedCompositeComponent), "PreparedComponent is prepared"

    prepare = get_prepare(PreparedCompositeComponent)
    assert callable(prepare), "getPrepare(PreparedCompositeComponent) is a function"
    import asyncio
    asyncio.run(prepare({'text': 'foo'}))

    assert prepareUsingProps_spy.call_count == 1, "prepareUsingProps called once"
    called_args = prepareUsingProps_spy.call_args[0][0]
    assert deep_equal(called_args, {'text': 'foo'}), "prepareUsingProps called with correct args"
    assert doAsyncSideEffect_spy.call_count == 1, "doAsyncSideEffect called exactly once"
    do_sideeffect_args = doAsyncSideEffect_spy.call_args[0][0]
    assert do_sideeffect_args == 'foo', "doAsyncSideEffect called with correct argument"

    rendered = PreparedCompositeComponent(text='foo').render()
    assert rendered == "<div>foo</div>", "renders with correct html"

def test_prepared_arrow_component():
    async def doAsyncSideEffect(text): pass
    doAsyncSideEffect_spy = MagicMock(side_effect=doAsyncSideEffect)

    async def prepareUsingProps(props):
        await doAsyncSideEffect_spy(props['text'])

    prepareUsingProps_spy = MagicMock(side_effect=prepareUsingProps)

    def OriginalArrowComponent(text):
        return f"<div>{text}</div>"

    class PreparedCompositeComponent(
        prepared(prepareUsingProps_spy)(OriginalArrowComponent)
    ):
        pass

    class PlainComponent: pass

    assert not is_prepared(PlainComponent), "OriginalComponent is not prepared"
    assert is_prepared(PreparedCompositeComponent), "PreparedComponent is prepared"

    prepare = get_prepare(PreparedCompositeComponent)
    assert callable(prepare), "getPrepare(PreparedCompositeComponent) is a function"
    import asyncio
    asyncio.run(prepare({'text': 'foo'}))

    assert prepareUsingProps_spy.call_count == 1, "prepareUsingProps called once"
    called_args = prepareUsingProps_spy.call_args[0][0]
    assert deep_equal(called_args, {'text': 'foo'}), "prepareUsingProps called with correct args"
    assert doAsyncSideEffect_spy.call_count == 1, "doAsyncSideEffect called exactly once"
    do_sideeffect_args = doAsyncSideEffect_spy.call_args[0][0]
    assert do_sideeffect_args == 'foo', "doAsyncSideEffect called with correct argument"

    rendered = PreparedCompositeComponent(text='foo').render()
    assert rendered == "<div>foo</div>", "renders with correct html"