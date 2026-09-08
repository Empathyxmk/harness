package public_tests

import (
	"testing"
	"strings"
	. "tests/original"
)

func TestEncode_SimpleString_Public(t *testing.T) {
	input := "Earth"
	expected := "5\r\nEarth\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestEncode_EmptyString_Public(t *testing.T) {
	input := ""
	expected := "0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestEncode_LongString_Public(t *testing.T) {
	input := "pqrstuvwxyz"
	expected := "b\r\npqrstuvwxyz\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}
func TestDecode_ValidChunked_Public(t *testing.T) {
	input := "4\r\nCode\r\n3\r\nGen\r\n0\r\n\r\n"
	expected := "CodeGen"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q", input, result, expected)
	}
}


func TestDecode_EmptyChunked_Public(t *testing.T) {
	input := "0\r\n\r\n"
	expected := ""
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_InvalidHex_Public(t *testing.T) {
	input := "QR\r\nfail\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (invalid hex)", input, result)
	}
}


func TestDecode_MissingCRLF_AfterChunkData_Public(t *testing.T) {
	input := "6\r\nplanet5\r\nEarth\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (missing CRLF after chunk data)", input, result)
	}
}

func TestDecode_ChunkWithExtensions_Public(t *testing.T) {
	input := "2;xy\r\nHi\r\n3;test\r\nSun\r\n0\r\n\r\n"
	expected := "HiSun"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (chunk extensions supported)", input, result, expected)
	}
}

func TestDecode_ExtraCRLF_BetweenChunks_Public(t *testing.T) {
	input := "1\r\ne\r\n\r\n2\r\nok\r\n0\r\n\r\n"
	expected := "eok"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (extra CRLF should be tolerated)", input, result, expected)
	}
}
func TestDecode_WithSpacesInChunkExt_Public(t *testing.T) {
	input := "4 ;a\r\nJava\r\n5\r\nTests\r\n0\r\n\r\n"
	expected := "JavaTests"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (spaces in chunk extensions)", input, result, expected)
	}
}

func TestDecode_WithDifferentChunkSizes_Public(t *testing.T) {
	input := "3\r\nbye\r\n1\r\n!\r\n2\r\nok\r\n0\r\n\r\n"
	expected := "bye!ok"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (multiple chunks of varying size)", input, result, expected)
	}
}

func TestDecode_NonASCII_Public(t *testing.T) {
	input := "2\r\nαβ\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (non-ASCII/multibyte)", input, result)
	}
}

func TestEncode_Unicode_Public(t *testing.T) {
	input := "测试"
	expected := "6\r\n测试\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q (unicode)", input, result, expected)
	}
}

func TestDecode_CapitalHex_Public(t *testing.T) {
	input := "B\r\n12345678901\r\n0\r\n\r\n"
	expected := "12345678901"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (capital hex OK)", input, result, expected)
	}
}

func TestDecode_LowercaseHex_Public(t *testing.T) {
	input := "9\r\nchunkdata\r\n0\r\n\r\n"
	expected := "chunkdata"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (lowercase hex OK)", input, result, expected)
	}
}

func TestEncode_CapitalAndLowercase_Public(t *testing.T) {
	input := "GenAI"
	expected := "5\r\nGenAI\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q", input, result, expected)
	}
}

func TestDecode_SingleChunk_Public(t *testing.T) {
	input := "4\r\nabcd\r\n0\r\n\r\n"
	expected := "abcd"
	result := Decode(input)
	if result != expected {
		t.Errorf("Decode(%q) = %q, want %q (single chunked block)", input, result, expected)
	}
}

func TestEncode_MultibyteCharacter_Public(t *testing.T) {
	input := "ø"
	expected := "2\r\nø\r\n0\r\n\r\n"
	result := Encode(input)
	if result != expected {
		t.Errorf("Encode(%q) = %q, want %q (multibyte)", input, result, expected)
	}
}

func TestDecode_UTF8_Public(t *testing.T) {
	input := "2\r\nλμ\r\n0\r\n\r\n"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (UTF-8 wrongly chunk-counted)", input, result)
	}
}

func TestDecode_TrailingCharactersAfterLastChunk_Public(t *testing.T) {
	input := "3\r\nxyz\r\n0\r\n\ntail"
	result := Decode(input)
	if result != "" {
		t.Errorf("Decode(%q) = %q, want nil/empty (junk found after finish)", input, result)
	}
}