from qcore import (
    convert_result,
    decorate,
    decorator_of_context_manager,
    DecoratorBase,
    deprecated,
    retry,
    get_original_fn,
    DecoratorBinder,
)
from qcore.asserts import assert_eq, assert_is, assert_in, assert_ne, AssertRaises
import inspect
import pickle
from unittest import mock

@deprecated("Not used anymore.")
def old_func():
    pass

@deprecated("Not used anymore.")
class OldClass:
    pass

def test_public_deprecated():
    fn = old_func
    fn.__doc__.startswith("Not used")
    deprecated("Not used anymore.")(5)

def test_public_convert_result():
    @convert_result(tuple)
    def test2(*args):
        for a in args:
            yield a
    result = test2(7, 4)
    assert_is(tuple, result.__class__)
    assert_eq((7, 4), result)

class SpecialException(Exception):
    pass

class AnotherException(Exception):
    pass

@retry(Exception)
def do_retry():
    pass

class TestPublicRetry:
    def mk_gen_fn(self, exception_type, max_tries):
        fn_body = mock.Mock()
        fn_body.return_value = range(2)

        @retry(exception_type, max_tries=max_tries)
        def some_fn(*args, **kwargs):
            for i in fn_body(*args, **kwargs):
                yield i
        return some_fn, fn_body

    def mk_fn(self, exception_type, max_tries):
        fn_body = mock.Mock()
        fn_body.return_value = []
        @retry(exception_type, max_tries=max_tries)
        def sample_fn(*args, **kwargs):
            return fn_body(*args, **kwargs)
        return sample_fn, fn_body

    def test_public_pickling(self):
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(do_retry, protocol=protocol)
            assert_is(do_retry, pickle.loads(pickled))

    def test_public_retry_args(self):
        e_type = SpecialException
        for m in (self.mk_fn, self.mk_gen_fn):
            sample_fn, fn_body = m(e_type, max_tries=3)
            list(sample_fn('a', foo='bar'))
            fn_body.assert_called_once_with('a', foo='bar')

    def test_public_retry_no_retry_on_success(self):
        e_type = SpecialException
        for m in (self.mk_fn, self.mk_gen_fn):
            fn, body = m(e_type, max_tries=2)
            list(fn())
            body.assert_called_once_with()

    def test_public_retry_no_retry_on_unexpected_exception(self):
        e_type = SpecialException
        wrong = AnotherException
        for m in (self.mk_fn, self.mk_gen_fn):
            fn, body = m(e_type, max_tries=2)
            body.side_effect = wrong
            with AssertRaises(wrong):
                list(fn())
            body.assert_called_once_with()

    def test_public_retry_on_exception(self):
        e_type = SpecialException
        tries = 2
        for m in (self.mk_fn, self.mk_gen_fn):
            fn, body = m(e_type, tries)
            body.side_effect = e_type
            with AssertRaises(e_type):
                list(fn())
            assert_eq(tries, body.call_count)

    def test_public_retry_requires_tries_at_least_one(self):
        e_type = SpecialException
        for m in (self.mk_fn, self.mk_gen_fn):
            with AssertRaises(Exception):
                m(e_type, max_tries=0)
            m(e_type, max_tries=1)

    def test_public_retry_multiple_exception_types(self):
        tries = 2
        e_type = SpecialException
        another_type = AnotherException
        for m in (self.mk_fn, self.mk_gen_fn):
            fn, body = m((e_type, another_type), tries)
            body.side_effect = another_type
            with AssertRaises(another_type):
                list(fn())
            assert_eq(tries, body.call_count)

            body.reset_mock()
            body.side_effect = e_type
            with AssertRaises(e_type):
                list(fn())
            assert_eq(tries, body.call_count)

    def test_public_retry_preserves_signature(self):
        def orig(foo, bar, baz=None, **kw):
            pass
        decorated = retry(Exception)(orig)
        assert_eq(inspect.signature(orig), inspect.signature(get_original_fn(decorated)))

def test_public_decorator_of_context_manager():
    data = []
    class AnotherContext:
        "Fake ctx"
        def __init__(self, marker):
            self.marker = marker
        def __enter__(self):
            data.append(">>>%s" % self.marker)
        def __exit__(self, *args):
            data.append("<<<%s" % self.marker)

    decorator = decorator_of_context_manager(AnotherContext)

    @decorator("omega")
    def decorated():
        data.append("mid omega")
    assert_eq("Fake ctx", decorator.__doc__)
    decorated()
    assert_eq([">>>omega", "mid omega", "<<<omega"], data)

    class NoDoc:
        def __enter__(self): pass
        def __exit__(self, *args): pass

    assert_eq(
        "Decorator that runs the inner function in the context of {}".format(
            NoDoc
        ),
        decorator_of_context_manager(NoDoc).__doc__,
    )

class JustAnotherDecorator(DecoratorBase):
    def name(self):
        return "JustAnotherDecorator"

def just_another_decorator(fn):
    return decorate(JustAnotherDecorator)(fn)

@just_another_decorator
def wrapped_fn():
    pass

def test_public_wrapped_fn_name():
    assert_in("test_public_decorators", wrapped_fn.__module__)

class TestDecoratorBinder(DecoratorBinder):
    def marker(self, *args):
        return self