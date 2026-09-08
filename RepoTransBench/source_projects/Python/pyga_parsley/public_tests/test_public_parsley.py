import unittest
import parsley


def wrapperFactory(multiplier):
    def wrapper(wrapped):
        return multiplier * 2, wrapped
    return wrapper

def nullFactory(*args):
    return tuple(reversed(args))


class StackTestCase(unittest.TestCase):
    def test_onlyBase(self):
        "stack can be called with no wrappers, using different base value and output."
        fac = parsley.stack(nullFactory)
        self.assertEqual(fac('b'), ('b',))

    def test_oneWrapper(self):
        "stack can be called with one wrapper and a different multiplication."
        fac = parsley.stack(wrapperFactory(3), nullFactory)
        self.assertEqual(fac('b'), (6, ('b',)))

    def test_tenWrappers(self):
        "stack can be called with ten wrappers, using different inputs."
        args = []
        result = 'b',
        for x in range(10):
            args.append(wrapperFactory(x + 1))
            result = 10 - x, result
        args.append(nullFactory)
        fac = parsley.stack(*args)
        self.assertEqual(fac('b'), result)

    def test_failsWithNoBaseSender(self):
        "stack does require at least the base factory (same logic, new context)."
        self.assertRaises(TypeError, parsley.stack)

    def test_senderFactoriesTakeOneArgument(self):
        "The callable returned by stack takes exactly one argument, tested differently."
        fac = parsley.stack(nullFactory)
        self.assertRaises(TypeError, fac)
        self.assertRaises(TypeError, fac, 'b', 'c')