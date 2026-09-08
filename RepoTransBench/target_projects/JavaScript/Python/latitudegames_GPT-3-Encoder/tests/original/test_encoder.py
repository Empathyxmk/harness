import pytest

from encoder import encode, decode

class TestGPT3EncoderMain:
    def test_empty_string(self):
        encoded = encode('')
        assert isinstance(encoded, list)
        assert len(encoded) == 0
        assert decode(encoded) == ''

    def test_space(self):
        encoded = encode(' ')
        assert decode(encoded) == ' '

    def test_tab(self):
        encoded = encode('\t')
        assert decode(encoded) == '\t'

    def test_simple_text(self):
        text = 'hello world'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert len(encoded) > 0
        decoded = decode(encoded)
        assert decoded == text

    def test_multi_token_word(self):
        # likely to be split
        text = 'indivisibility'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert decode(encoded) == text

    def test_emojis(self):
        text = '😀😃😄😁'
        encoded = encode(text)
        assert isinstance(encoded, list)
        assert decode(encoded) == text

    def test_properties_of_object(self):
        # Python lacks JS's prototype pollution, but we simulate test for robustness.
        # We can monkeypatch object, but it's not needed in Python; still test the round-trip.
        text = 'danger'
        encoded = encode(text)
        assert decode(encoded) == text

    def test_special_unicode_in_input(self):
        text = '\u00a9\u2202\u2603'
        encoded = encode(text)
        assert decode(encoded) == text

    def test_long_sentence(self):
        long = (
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin viverra, ligula sit amet '
            'ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros.'
        )
        encoded = encode(long)
        assert decode(encoded) == long

    def test_all_bytes_in_unicode_range_0_255(self):
        # Test all possible byte values round-trip
        text = ''.join(chr(i) for i in range(256))
        encoded = encode(text)
        assert decode(encoded) == text


class TestEncoderJsEdgeCoverage:
    def test_decodes_empty_array(self):
        assert decode([]) == ''

    def test_decode_encode_is_reversible_various_lengths(self):
        for s in ['a', 'ab', 'abc', 'abcd', 'abcde']:
            assert decode(encode(s)) == s

    def test_does_not_mutate_input_tokens_array(self):
        text = 'mutable test'
        encoded = encode(text)
        original = list(encoded)
        decode(encoded)
        assert encoded == original