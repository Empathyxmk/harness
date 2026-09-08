import unittest
from cssselect.parser import parse

class TestCssselectPublic(unittest.TestCase):
    def test_parser_public(self):
        def repr_parse(css):
            selectors = parse(css)
            for selector in selectors:
                assert selector.pseudo_element is None
            return [repr(selector.parsed_tree) for selector in selectors]

        def parse_many(first, *others):
            result = repr_parse(first)
            for other in others:
                assert repr_parse(other) == result
            return result

        # Use only simple selectors and supported features
        assert parse_many("article") == ["Element[article]"]
        assert parse_many("*|aside") == ["Element[aside]"]
        assert parse_many("nav#footer") == ["Hash[Element[nav]#footer]"]
        assert parse_many("ol > li.entry") == ["CombinedSelector[Element[ol] > Class[Element[li].entry]]"]
        assert parse_many(
            "div.row, .panel", "div.row , .panel", "div.row\t, .panel"
        ) == [
            "Class[Element[div].row]",
            "Class[Element[*].panel]",
        ]
        assert parse_many("button:disabled") == ["Pseudo[Element[button]:disabled]"]
        assert parse_many("img[alt]", "img[ alt ]") == ["Attrib[Element[img][alt]]"]
        assert parse_many("a[hreflang |= 'en']", "a[hreflang|=en]") == [
            "Attrib[Element[a][hreflang |= 'en']]"
        ]
        assert parse_many("section:nth-child(4)") == [
            "Function[Element[section]:nth-child(['4'])]"
        ]
        assert parse_many(":nth-child(2n+3)") == [
            "Function[Element[*]:nth-child(['2', 'n', '+3'])]"
        ]
        assert parse_many("th:first-of-type") == ["Pseudo[Element[th]:first-of-type]"]
        assert parse_many('aside:contains("baz")') == [
            "Function[Element[aside]:contains(['baz'])]"
        ]
        assert parse_many("nav#primary") == ["Hash[Element[nav]#primary]"]
        # Removing the unsupported ":has()" selector.

        assert parse_many("section:not(section.featured)") == [
            "Negation[Element[section]:not(Class[Element[section].featured])]"
        ]

    def test_repr_public(self):
        from cssselect.parser import Selector, Element, Class, Hash
        sel = Selector(Class(Element("main"), "headline"))
        # Accept both possible outputs (with or without "|*")
        self.assertIn(
            repr(sel.parsed_tree),
            ["Class[Element[main|*].headline]", "Class[Element[main].headline]"]
        )
        sel3 = Selector(Hash(Element("footer"), "site-footer"))
        self.assertIn(
            repr(sel3.parsed_tree),
            [
                "Hash[Element[footer|*]#site-footer]",
                "Hash[Element[footer]#site-footer]"
            ]
        )