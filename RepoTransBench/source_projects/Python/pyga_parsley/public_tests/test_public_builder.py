from textwrap import dedent
import unittest

from ometa.builder import writePython
from terml.nodes import termMaker as t
from terml.parser import parseTerm as term

def dd(txt):
    return dedent(txt).strip()

class PublicPythonWriterTests(unittest.TestCase):
    """
    Tests for generating Python source from an AST (public, different test data).
    """

    def test_exactly(self):
        y = t.Exactly("y")
        self.assertEqual(writePython(y ,""),
                         dd("""
                            _G_exactly_1, lastError = self.exactly('y')
                            self.considerError(lastError, None)
                            _G_exactly_1
                            """))

    def test_apply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.Apply("bar", "main", [two, y])
        self.assertEqual(writePython(a, ""),
                         dd("""
                            _G_python_1, lastError = (2), None
                            self.considerError(lastError, None)
                            _G_python_2, lastError = eval('y', self.globals, _locals), None
                            self.considerError(lastError, None)
                            _G_apply_3, lastError = self._apply(self.rule_bar, "bar", [_G_python_1, _G_python_2])
                            self.considerError(lastError, None)
                            _G_apply_3
                            """))

    def test_foreignApply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.ForeignApply("othergrammar", "bar", "main", [two, y])
        self.assertEqual(writePython(a, ""),
                         dd("""
                            _G_python_1, lastError = (2), None
                            self.considerError(lastError, None)
                            _G_python_2, lastError = eval('y', self.globals, _locals), None
                            self.considerError(lastError, None)
                            _G_apply_3, lastError = self.foreignApply("othergrammar", "bar", self.globals, _locals, _G_python_1, _G_python_2)
                            self.considerError(lastError, None)
                            _G_apply_3
                            """))

    def test_superApply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.Apply("super", "main", [two, y])
        self.assertEqual(writePython(a, ""),
                         dd("""
                            _G_python_1, lastError = (2), None
                            self.considerError(lastError, None)
                            _G_python_2, lastError = eval('y', self.globals, _locals), None
                            self.considerError(lastError, None)
                            _G_apply_3, lastError = self.superApply("main", _G_python_1, _G_python_2)
                            self.considerError(lastError, None)
                            _G_apply_3
                            """))

    def test_many(self):
        ys = t.Many(t.Exactly("y"))
        self.assertEqual(writePython(ys, ""),
                         dd("""
                            def _G_many_1():
                                _G_exactly_2, lastError = self.exactly('y')
                                self.considerError(lastError, None)
                                return (_G_exactly_2, self.currentError)
                            _G_many_3, lastError = self.many(_G_many_1)
                            self.considerError(lastError, None)
                            _G_many_3
                            """))

    def test_many1(self):
        ys = t.Many1(t.Exactly("y"))
        self.assertEqual(writePython(ys, ""),
                         dd("""
                            def _G_many1_1():
                                _G_exactly_2, lastError = self.exactly('y')
                                self.considerError(lastError, None)
                                return (_G_exactly_2, self.currentError)
                            _G_many1_3, lastError = self.many(_G_many1_1, _G_many1_1())
                            self.considerError(lastError, None)
                            _G_many1_3
                            """))

    def test_or(self):
        yz = t.Or([t.Exactly("y"),
                   t.Exactly("z")])
        self.assertEqual(writePython(yz, ""),
                         dd("""
                            def _G_or_1():
                                _G_exactly_2, lastError = self.exactly('y')
                                self.considerError(lastError, None)
                                return (_G_exactly_2, self.currentError)
                            def _G_or_3():
                                _G_exactly_4, lastError = self.exactly('z')
                                self.considerError(lastError, None)
                                return (_G_exactly_4, self.currentError)
                            _G_or_5, lastError = self._or([_G_or_1, _G_or_3])
                            self.considerError(lastError, None)
                            _G_or_5
                            """))

    def test_singleOr(self):
        y1 = t.Or([t.Exactly("y")])
        y = t.Exactly("y")
        self.assertEqual(writePython(y, ""), writePython(y1, ""))

    def test_optional(self):
        y = t.Optional(t.Exactly("y"))
        self.assertEqual(writePython(y, ""),
                         dd("""
                            def _G_optional_1():
                                _G_exactly_2, lastError = self.exactly('y')
                                self.considerError(lastError, None)
                                return (_G_exactly_2, self.currentError)
                            def _G_optional_3():
                                return (None, self.input.nullError())
                            _G_or_4, lastError = self._or([_G_optional_1, _G_optional_3])
                            self.considerError(lastError, None)
                            _G_or_4
                            """))

    def test_not(self):
        y = t.Not(t.Exactly("y"))
        self.assertEqual(writePython(y ,""),
                         dd("""
                            def _G_not_1():
                                _G_exactly_2, lastError = self.exactly('y')
                                self.considerError(lastError, None)
                                return (_G_exactly_2, self.currentError)
                            _G_not_3, lastError = self._not(_G_not_1)
                            self.considerError(lastError, None)
                            _G_not_3
                            """))