from unittest import TestCase
from terml.nodes import termMaker as t
from ometa.vm_builder import writeBytecode, writeBytecodeRule, writeBytecodeGrammar

class PublicTestVMBuilder(TestCase):
    def test_exactly(self):
        y = t.Exactly("b")
        self.assertEqual(writeBytecode(y),
                         [t.Match("b")])

    def test_apply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.Apply("bar", "main", [two, y])
        self.assertEqual(writeBytecode(a),
                         [t.Python('2'),
                          t.Push(),
                          t.Python('y'),
                          t.Push(),
                          t.Call('bar')])

    def test_foreignApply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.ForeignApply("othergrammar", "bar", "main", [two, y])
        self.assertEqual(writeBytecode(a),
                         [t.Python('2'),
                          t.Push(),
                          t.Python('y'),
                          t.Push(),
                          t.ForeignCall('othergrammar', 'bar')])

    def test_superApply(self):
        two = t.Action("2")
        y = t.Action("y")
        a = t.Apply("super", "main", [two, y])
        self.assertEqual(writeBytecode(a),
                         [t.Python('2'),
                          t.Push(),
                          t.Python('y'),
                          t.Push(),
                          t.SuperCall('main')])

    def test_many(self):
        ys = t.Many(t.Exactly("y"))
        self.assertEqual(writeBytecode(ys),
                         [t.Choice(3),
                          t.Match("y"),
                          t.Commit(-2)])

    def test_many1(self):
        ys = t.Many1(t.Exactly("y"))
        self.assertEqual(writeBytecode(ys),
                         [t.Match('y'),
                          t.Choice(3),
                          t.Match('y'),
                          t.Commit(-2)])

    def test_tripleOr(self):
        yz = t.Or([t.Exactly("y"),
                   t.Exactly("z"),
                   t.Exactly("q")])
        self.assertEqual(writeBytecode(yz),
                         [t.Choice(3),
                          t.Match('y'),
                          t.Commit(5),
                          t.Choice(3),
                          t.Match('z'),
                          t.Commit(2),
                          t.Match('q')])

    def test_doubleOr(self):
        yz = t.Or([t.Exactly("y"),
                   t.Exactly("z")])
        self.assertEqual(writeBytecode(yz),
                         [t.Choice(3),
                          t.Match('y'),
                          t.Commit(2),
                          t.Match('z')])

    def test_singleOr(self):
        y1 = t.Or([t.Exactly("y")])
        y = t.Exactly("y")
        self.assertEqual(writeBytecode(y1),
                         writeBytecode(y))

    def test_optional(self):
        y = t.Optional(t.Exactly("y"))
        self.assertEqual(writeBytecode(y),
                         [t.Choice(3),
                          t.Match('y'),
                          t.Commit(2),
                          t.Python("None")])

    def test_not(self):
        y = t.Not(t.Exactly("y"))
        self.assertEqual(writeBytecode(y),
                         [t.Choice(4),
                          t.Match('y'),
                          t.Commit(1),
                          t.Fail()])

    def test_lookahead(self):
        y = t.Lookahead(t.Exactly("y"))
        self.assertEqual(writeBytecode(y),
                         [t.Choice(7),
                          t.Choice(4),
                          t.Match('y'),
                          t.Commit(1),
                          t.Fail(),
                          t.Commit(1),
                          t.Fail()])

    def test_sequence(self):
        y = t.Exactly("y")
        z = t.Exactly("z")
        q = t.And([y, z])
        self.assertEqual(writeBytecode(q),
                         [t.Match('y'),
                          t.Match('z')])

    def test_bind(self):
        y = t.Exactly("y")
        b = t.Bind("var2", y)
        self.assertEqual(writeBytecode(b),
                         [t.Match('y'),
                          t.Bind('var2')])

    def test_bind_apply(self):
        y = t.Apply("members", "object", [])
        b = t.Bind("n", y)
        self.assertEqual(writeBytecode(b),
                         [t.Call('members'),
                          t.Bind('n')])

    def test_pred(self):
        y = t.Predicate(t.Action("doOtherStuff()"))
        self.assertEqual(writeBytecode(y),
                         [t.Python('doOtherStuff()'),
                          t.Predicate()])

    def test_listpattern(self):
        y = t.List(t.Exactly("y"))
        self.assertEqual(writeBytecode(y),
                         [t.Descend(),
                          t.Match('y'),
                          t.Ascend()])

    def test_rule(self):
        y = t.Rule("bar", t.Exactly("y"))
        k, v = writeBytecodeRule(y)
        self.assertEqual(k, "bar")
        self.assertEqual(v, [t.Match('y')])

    def test_grammar(self):
        r1 = t.Rule("bar", t.Exactly("y"))
        r2 = t.Rule("foo", t.Exactly("z"))
        y = t.Grammar("PublicBuilderTest", False, [r1, r2])
        g = writeBytecodeGrammar(y)
        self.assertEqual(sorted(g.keys()), ['bar', 'foo'])
        self.assertEqual(g['bar'], [t.Match('y')])
        self.assertEqual(g['foo'], [t.Match('z')])

    def test_repeat(self):
        y = t.Repeat(2, 5, t.Exactly('y'))
        self.assertEqual(writeBytecode(y),
                         [t.Python("2"),
                          t.Push(),
                          t.Python("5"),
                          t.Push(),
                          t.RepeatChoice(3),
                          t.Match('y'),
                          t.Commit(-2)])

    def test_consumedby(self):
        y = t.ConsumedBy(t.Exactly('y'))
        self.assertEqual(writeBytecode(y),
                         [t.StartSlice(),
                          t.Match('y'),
                          t.EndSlice()])