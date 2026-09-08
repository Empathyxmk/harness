import pytest

from encoder import encode, decode

class TestGPT3EncoderMainPublic:
    def test_single_character(self):
        encoded = encode('x')
        assert isinstance(encoded, list)
        assert len(encoded) == 1
        assert decode(encoded) == 'x'

    def test_newline(self):
        encoded = encode('\n')
        assert decode(encoded) == '\n'

    def test_carriage_return(self):
        encoded = encode('\r')
        assert decode(encoded) == '\r'

    def test_different_simple_text(self):
        text = 'test string'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert len(encoded) > 0
        decoded = decode(encoded)
        assert decoded == text

    def test_another_multi_token_word(self):
        # likely to be split
        text = 'unbelievability'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert decode(encoded) == text

    def test_different_emojis(self):
        text = '😎🤓🧐🥸'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert decode(encoded) == text

    def test_properties_of_array_prototype(self):
        # Python does not have array prototype properties, but test round-trip for robustness
        text = 'hazard'
        encoded = encode(text)
        assert decode(encoded) == text

    def test_other_special_unicode_in_input(self):
        text = '\u263A\u265E\u2665'  # ☺♞♥
        encoded = encode(text)
        assert decode(encoded) == text

    def test_another_long_sentence(self):
        long = (
            'Quick brown fox jumps over the lazy dog, testing encoding with varied characters... Wow!'
        )
        encoded = encode(long)
        assert decode(encoded) == long

    def test_all_printable_ascii_chars_32_126(self):
        # Test all printable ASCII chars round-trip
        text = ''.join(chr(i+32) for i in range(95))
        encoded = encode(text)
        assert decode(encoded) == text


class TestEncoderJsEdgeCoveragePublic:
    def test_decodes_array_with_no_elements(self):
        assert decode([]) == ''

    def test_decode_encode_is_reversible_for_various_different_strings(self):
        for s in ['z', 'yz', 'wxyz', 'mnop', 'qrstu']:
            assert decode(encode(s)) == s

    def test_does_not_mutate_input_tokens_array_for_different_text(self):
        text = 'immutability check'
        encoded = encode(text)
        original = list(encoded)
        decode(encoded)
        assert encoded == original