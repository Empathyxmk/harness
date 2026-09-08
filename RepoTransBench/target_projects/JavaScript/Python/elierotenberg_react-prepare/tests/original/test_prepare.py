import pytest
from unittest.mock import MagicMock
from deepdiff import DeepDiff

def deep_equal(a, b):
    return not DeepDiff(a, b, ignore_order=True)

# Dummy React/PropTypes/prepare/prepared emulation.

class DummyComponent:
    propTypes = {}
    def __init__(self, **kwargs):
        self.props = kwargs
        self.state = None
        self.updater = True
        self.refs = {}
        self.context = {}

    def setState(self, new_state):
        if self.state is None:
            self.state = {}
        self.state.update(new_state)

    def render(self):
        return None

def renderToStaticMarkup(component):
    # Simulate render, just call .render() and return something based on that
    return component.render()

def prepare(component):
    # Simulate async prepare
    import asyncio
    async def _noop(*args, **kwargs):
        pass
    return asyncio.run(_noop())

def test_sets_instance_properties():
    class MessageBox(DummyComponent):
        propTypes = {'message': str}
        def render(self):
            assert deep_equal(self.props, {'message': 'Hello'}), "sets props on instance"
            assert self.state is None, "sets state on instance"
            assert self.updater is not None, "sets updater on instance"
            assert deep_equal(self.refs, {}), "sets refs on instance"
            assert deep_equal(self.context, {}), "sets context on instance"
            return None
    renderToStaticMarkup(MessageBox(message='Hello'))
    prepare(MessageBox(message='Hello'))

def test_supports_state_updates_in_component_will_mount():
    class MessageBox(DummyComponent):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.state = {'message': 'Hello'}
        def componentWillMount(self):
            self.setState({'message': 'Updated message'})
        def render(self):
            assert self.state['message'] == 'Updated message', "updates state on instance"
            return None
    msg = MessageBox()
    msg.componentWillMount()
    renderToStaticMarkup(msg)
    prepare(msg)

def test_shallow_hierarchy_no_children():
    async def doAsyncSideEffect(): pass
    doAsyncSideEffect_spy = MagicMock(side_effect=doAsyncSideEffect)
    async def prepareUsingProps(props):
        await doAsyncSideEffect_spy(props['text'])

    prepareUsingProps_spy = MagicMock(side_effect=prepareUsingProps)

    class App:
        def __init__(self, text):
            self.text = text
        def __call__(self):
            return f"<div>{self.text}</div>"

    import asyncio
    asyncio.run(prepareUsingProps_spy({'text': 'foo'}))

    assert prepareUsingProps_spy.call_count == 1
    called_args = prepareUsingProps_spy.call_args[0][0]
    assert deep_equal(called_args, {'text': 'foo'}), "called correct args"
    doAsyncSideEffect_spy.assert_called_once()
    do_sideeffect_args = doAsyncSideEffect_spy.call_args[0][0]
    assert do_sideeffect_args == 'foo'
    html = App('foo')()
    assert html == "<div>foo</div>"

def test_deep_hierarchy():
    class_name_of_first = 'FirstChild'
    class_name_of_second = 'SecondChild'

    async def doAsyncSideEffectForFirstChild(text):
        nonlocal class_name_of_first
        class_name_of_first = 'prepared(FirstChild)'

    async def prepareUsingPropsForFirstChild(props):
        await doAsyncSideEffectForFirstChild(props['text'])

    doAsyncFirst_spy = MagicMock(side_effect=doAsyncSideEffectForFirstChild)
    prepareFirst_spy = MagicMock(side_effect=prepareUsingPropsForFirstChild)

    async def doAsyncSideEffectForSecondChild(text):
        nonlocal class_name_of_second
        class_name_of_second = 'prepared(SecondChild)'

    async def prepareUsingPropsForSecondChild(props):
        await doAsyncSideEffectForSecondChild(props['text'])

    doAsyncSecond_spy = MagicMock(side_effect=doAsyncSideEffectForSecondChild)
    prepareSecond_spy = MagicMock(side_effect=prepareUsingPropsForSecondChild)

    class FirstChild:
        def __init__(self, text):
            self.text = text
        def __call__(self):
            return f'<span class="{class_name_of_first}">{self.text}</span>'

    class SecondChild:
        def __init__(self, text):
            self.text = text
        def __call__(self):
            return f'<span class="{class_name_of_second}">{self.text}</span>'

    class App:
        def __init__(self, texts):
            self.texts = texts
        def __call__(self):
            return (
                "<ul>"
                f'<li>{FirstChild(self.texts[0])()}</li>'
                f'<li>{SecondChild(self.texts[1])()}</li>'
                "</ul>"
            )

    import asyncio
    asyncio.run(prepareFirst_spy({'text': 'first'}))
    asyncio.run(prepareSecond_spy({'text': 'second'}))

    assert prepareFirst_spy.call_count == 1
    assert prepareSecond_spy.call_count == 1
    arg1 = prepareFirst_spy.call_args[0][0]
    assert deep_equal(arg1, {'text': 'first'}), "firstchild correct args"
    arg2 = prepareSecond_spy.call_args[0][0]
    assert deep_equal(arg2, {'text': 'second'}), "secondchild correct args"
    doAsyncFirst_spy.assert_called_once()
    doAsyncSecond_spy.assert_called_once()

    html = App(['first', 'second'])()
    assert (
        html
        == '<ul><li><span class="prepared(FirstChild)">first</span></li><li><span class="prepared(SecondChild)">second</span></li></ul>'
    )