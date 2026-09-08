import pytest

class DoctrineParseException(Exception):
    pass

class DoctrineKindException(Exception):
    pass

class DoctrineVariationException(Exception):
    pass

class DoctrineAccessException(Exception):
    pass

# Mock implementation to simulate exceptions for strict parsing
def doctrine_parse(comment, opts=None):
    text = "\n".join(comment) if isinstance(comment, list) else comment
    if opts and opts.get('strict'):
        if "{" in text and "}" not in text:
            raise DoctrineParseException('Braces are not balanced')
        if "@@" in text:
            raise DoctrineParseException('Missing or invalid title')
        if "@kind publicAPI" in text:
            raise DoctrineKindException("Invalid kind name 'publicAPI'")
        if "@variation Beta" in text:
            raise DoctrineVariationException("Invalid variation 'Beta'")
        if "@access internal" in text:
            raise DoctrineAccessException("Invalid access name 'internal'")

describe_cases = [
    {
        "comment": [
            "/**",
            " * @return {num",
            " */"
        ],
        "exception": DoctrineParseException,
        "message": "Braces are not balanced"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @prop {array name Prop description",
            " * @prop {Object} bar Prop bar",
            " */"
        ],
        "exception": DoctrineParseException,
        "message": "Braces are not balanced"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @yields {float",
            " */"
        ],
        "exception": DoctrineParseException,
        "message": "Braces are not balanced"
    },
]

describe_cases_at = [
    {
        "comment": [
            "/**",
            " * @@version_info",
            " */"
        ],
        "exception": DoctrineParseException,
        "message": "Missing or invalid title"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @@throws {Error} reason for throwing",
            " */"
        ],
        "exception": DoctrineParseException,
        "message": "Missing or invalid title"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @kind publicAPI",
            " */"
        ],
        "exception": DoctrineKindException,
        "message": "Invalid kind name 'publicAPI'"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @variation Beta",
            " */"
        ],
        "exception": DoctrineVariationException,
        "message": "Invalid variation 'Beta'"
    },
    {
        "comment": [
            "/**",
            " * Description",
            " * @access internal",
            " */"
        ],
        "exception": DoctrineAccessException,
        "message": "Invalid access name 'internal'"
    },
]

class TestStrictParsePublic:
    def test_unbalanced_braces(self):
        for case in describe_cases:
            with pytest.raises(case['exception'], match=case['message']):
                doctrine_parse(case['comment'], {'unwrap': True, 'strict': True})

            doctrine_parse(case['comment'], {'unwrap': True})  # should not throw

    def test_incorrect_tag_starting_with_atat(self):
        for case in describe_cases_at:
            if "@@" in "\n".join(case['comment']) or "@kind publicAPI" in "\n".join(case['comment']) or "@variation Beta" in "\n".join(case['comment']) or "@access internal" in "\n".join(case['comment']):
                with pytest.raises(case['exception'], match=case['message']):
                    doctrine_parse(case['comment'], {'unwrap': True, 'strict': True})

                doctrine_parse(case['comment'], {'unwrap': True})  # should not throw except for kind, variation, access which require strict only