import unittest

def replace_alternate_color_code(data: str, alt_char: str, color_char: str) -> str:
    # Emulate ARRCON::helpers::replace_alternate_color_code in Python:
    # Replace every occurrence of (color_char)(alt_char)X with (§)X
    # Example: '#d' (with alt_char='#', color_char='&') -> '§d'
    # C++ code replaced each color_char+alt_char+code with §+code
    # See test for string: "&#d Hello"
    out = ""
    i = 0
    while i < len(data):
        if data[i] == color_char and i + 1 < len(data) and data[i+1] == alt_char:
            # Replace: &#
            if i + 2 < len(data):
                code_char = data[i+2]
                out += '§' + code_char
                i += 3
                continue
        out += data[i]
        i += 1
    return out

class TestPublicBukkitColors(unittest.TestCase):
    def test_public_alternate_color_code(self):
        data = "&#d Hello"
        result = replace_alternate_color_code(data, '#', '&')
        self.assertEqual(result, "§d Hello")

    def test_public_no_replacement_if_not_present(self):
        data = "abc123"
        result = replace_alternate_color_code(data, '#', '&')
        self.assertEqual(result, "abc123")