package original

import (
	"testing"
	"reflect"
	"strings"
)

// Reference to the main conversion functions:
// ChunkedCodingConverter.encode and decode;
// We'll implement a stub "chunkedcodingconverter.go" file under "tests/original/" for testability

func TestEncode_SimpleString(t *testing.T) {
	input := "Hello"
	expected := "5\r\nHello\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestEncode_EmptyString(t *testing.T) {
	input := ""
	expected := "0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestEncode_LongString(t *testing.T) {
	input := "abcdefghijklmnopqrstuvwxyz"
	expected := "1a\r\nabcdefghijklmnopqrstuvwxyz\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_ValidChunked(t *testing.T) {
	input := "5\r\nHello\r\n5\r\nWorld\r\n0\r\n\r\n"
	expected := "HelloWorld"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_EmptyChunked(t *testing.T) {
	input := "0\r\n\r\n"
	expected := ""
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_InvalidHex(t *testing.T) {
	input := "GG\r\nInvalid\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (invalid hex)", input, result)
	}
}

func TestDecode_MissingCRLF_AfterChunkData(t *testing.T) {
	input := "5\r\nHello6\r\nWorld!\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (missing CRLF after chunk data)", input, result)
	}
}

func TestDecode_ChunkWithExtensions(t *testing.T) {
	input := "4;xtest\r\nTest\r\n3 ;xfoo\r\nAbc\r\n0\r\n\r\n"
	expected := "TestAbc"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (chunk extensions supported)", input, result, expected)
	}
}

func TestDecode_ExtraCRLF_BetweenChunks(t *testing.T) {
	input := "3\r\nHey\r\n\r\n2\r\nYo\r\n0\r\n\r\n"
	expected := "HeyYo"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (extra CRLF should be tolerated)", input, result, expected)
	}
}

func TestDecode_WithSpacesInChunkExt(t *testing.T) {
	input := "5 ;bar=10\r\nApple\r\n4\r\nTest\r\n0\r\n\r\n"
	expected := "AppleTest"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (spaces in chunk extensions)", input, result, expected)
	}
}

func TestDecode_WithDifferentChunkSizes(t *testing.T) {
	input := "2\r\nAB\r\n3\r\nCDE\r\n1\r\nF\r\n0\r\n\r\n"
	expected := "ABCDEF"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (multiple chunks of varying size)", input, result, expected)
	}
}

func TestDecode_NonASCII(t *testing.T) {
	input := "6\r\n你好吗\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (non-ASCII/multibyte characters are miscounted)", input, result)
	}
}

func TestEncode_Unicode(t *testing.T) {
	input := "你好吗"
	expected := "9\r\n你好吗\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q (unicode, but counts runes)", input, result, expected)
	}
}

func TestDecode_CapitalHex(t *testing.T) {
	input := "A\r\n1234567890\r\n0\r\n\r\n"
	expected := "1234567890"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (capital hex OK)", input, result, expected)
	}
}

func TestDecode_LowercaseHex(t *testing.T) {
	input := "a\r\nabcdefghij\r\n0\r\n\r\n"
	expected := "abcdefghij"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (lowercase hex OK)", input, result, expected)
	}
}

func TestEncode_CapitalAndLowercase(t *testing.T) {
	input := "AbCdEf"
	expected := "6\r\nAbCdEf\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_SingleChunk(t *testing.T) {
	input := "8\r\n12345678\r\n0\r\n\r\n"
	expected := "12345678"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (single chunked block)", input, result, expected)
	}
}

func TestEncode_MultibyteCharacter(t *testing.T) {
	input := "ß" // U+00DF, UTF-8: C3 9F
	expected := "2\r\nß\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q (multibyte, counted as bytes)", input, result, expected)
	}
}

func TestDecode_UTF8(t *testing.T) {
	input := "2\r\n你好\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (UTF-8 wrongly chunk-counted)", input, result)
	}
}

func TestDecode_TrailingCharactersAfterLastChunk(t *testing.T) {
	input := "5\r\nHello\r\n0\r\n\r\nabc"
	expected := "Hello"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (should ignore trailing after correct finish)", input, result, expected)
	}
}