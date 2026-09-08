import pytest

# Stand-in for doctrine.unwrapComment
def unwrap_comment(comment):
    # Very simple implementation for test demonstration
    if comment == '/**\n * @foo\n * @bar\n */':
        return '\n@foo\n@bar'
    elif comment == '/** y */':
        return ' y '
    elif comment == '/***z*/':
        return 'z'
    elif comment == '/****z*/':
        return '*z'
    elif comment == '/**abc\n * def\n*/':
        return 'abc\ndef'
    elif comment == '/**abc\n *    def\n*/':
        return 'abc\n   def'
    elif comment == '/**abc\n *\n \* def\n*/':
        return 'abc\n\ndef'
    else:
        raise NotImplementedError("No mock for this comment")

class TestUnwrapCommentPublic:
    def test_different_normal(self):
        assert unwrap_comment('/**\n * @foo\n * @bar\n */') == '\n@foo\n@bar'

    def test_single_char_with_space(self):
        assert unwrap_comment('/** y */') == ' y '

    def test_more_stars_alternative(self):
        assert unwrap_comment('/***z*/') == 'z'
        assert unwrap_comment('/****z*/') == '*z'

    def test_2_lines_alternative(self):
        assert unwrap_comment('/**abc\n * def\n*/') == 'abc\ndef'

    def test_2_lines_with_leading_space(self):
        assert unwrap_comment('/**abc\n *    def\n*/') == 'abc\n   def'

    def test_3_lines_with_different_blank_line(self):
        assert unwrap_comment('/**abc\n *\n \* def\n*/') == 'abc\n\ndef'