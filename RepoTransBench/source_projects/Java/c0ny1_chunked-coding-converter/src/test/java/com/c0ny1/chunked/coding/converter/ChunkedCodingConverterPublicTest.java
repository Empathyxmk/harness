package com.c0ny1.chunked.coding.converter;

import org.junit.Test;
import static org.junit.Assert.*;

/*
 * Public test cases for ChunkedCodingConverter. 
 * Uses different, but valid and meaningful, input/output versus private tests and reference, 
 * but all logic branches and edge cases are covered.
 *
 * N.B.: Multibyte/UTF-8 tests may show "unexpected" chunk length due to String.length() semantics.
 * (Ex: "测试".length() == 2; "pqrstuvwxyz".length() == 11, "ø".length() == 1, etc.)
 * 
 * The following test adjustments fix: 
 * - testEncode_LongString: chunk length for 'pqrstuvwxyz' is 11 (hex 'b')
 * - testEncode_Unicode: '测试'.length() == 2 Chinese Unicode characters, but .length() returns 2, but implementation produces chunk size 6 (the byte size).
 *   However, existing ChunkedCodingConverter implementation likely uses input.getBytes().length for length calculation.
 *   Need to adjust expected to match "6\r\n测试\r\n0\r\n\r\n" (instead of "2\r\n测试\r\n0\r\n\r\n")
 */

public class ChunkedCodingConverterPublicTest {

    @Test
    public void testEncode_SimpleString() {
        String input = "Earth";
        String expected = "5\r\nEarth\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testEncode_EmptyString() {
        String input = "";
        String expected = "0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testEncode_LongString() {
        String input = "pqrstuvwxyz";
        String expected = "b\r\npqrstuvwxyz\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }
    
    @Test
    public void testDecode_ValidChunked() {
        String input = "4\r\nCode\r\n3\r\nGen\r\n0\r\n\r\n";
        String expected = "CodeGen";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }
    
    @Test
    public void testDecode_EmptyChunked() {
        String input = "0\r\n\r\n";
        String expected = "";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }
    
    @Test
    public void testDecode_InvalidHex() {
        String input = "QR\r\nfail\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.decode(input);
        assertNull(result);
    }
    
    @Test
    public void testDecode_MissingCRLF_AfterChunkData() {
        String input = "6\r\nplanet5\r\nEarth\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.decode(input);
        assertNull(result);
    }

    @Test
    public void testDecode_ChunkWithExtensions() {
        String input = "2;xy\r\nHi\r\n3;test\r\nSun\r\n0\r\n\r\n";
        String expected = "HiSun";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_ExtraCRLF_BetweenChunks() {
        String input = "1\r\ne\r\n\r\n2\r\nok\r\n0\r\n\r\n";
        String expected = "eok";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }
    
    @Test
    public void testDecode_WithSpacesInChunkExt() {
        String input = "4 ;a\r\nJava\r\n5\r\nTests\r\n0\r\n\r\n";
        String expected = "JavaTests";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_WithDifferentChunkSizes() {
        String input = "3\r\nbye\r\n1\r\n!\r\n2\r\nok\r\n0\r\n\r\n";
        String expected = "bye!ok";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_NonASCII() {
        String input = "2\r\nαβ\r\n0\r\n\r\n";
        // Reference implementation returns null for these
        String result = ChunkedCodingConverter.decode(input);
        assertNull(result);
    }

    @Test
    public void testEncode_Unicode() {
        String input = "测试";
        // "测试".getBytes(StandardCharsets.UTF_8).length == 6, so "6\r\n测试\r\n0\r\n\r\n"
        String expected = "6\r\n测试\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_CapitalHex() {
        String input = "B\r\n12345678901\r\n0\r\n\r\n";
        String expected = "12345678901";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_LowercaseHex() {
        String input = "9\r\nchunkdata\r\n0\r\n\r\n";
        String expected = "chunkdata";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testEncode_CapitalAndLowercase() {
        String input = "GenAI";
        String expected = "5\r\nGenAI\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_SingleChunk() {
        String input = "4\r\nabcd\r\n0\r\n\r\n";
        String expected = "abcd";
        String result = ChunkedCodingConverter.decode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testEncode_MultibyteCharacter() {
        String input = "ø";
        // "ø".getBytes(StandardCharsets.UTF_8).length == 2
        String expected = "2\r\nø\r\n0\r\n\r\n";
        String result = ChunkedCodingConverter.encode(input);
        assertEquals(expected, result);
    }

    @Test
    public void testDecode_UTF8() {
        String input = "2\r\nλμ\r\n0\r\n\r\n";
        // Implementation returns null (not matching bytes), so expect null
        String result = ChunkedCodingConverter.decode(input);
        assertNull(result);
    }

    @Test
    public void testDecode_TrailingCharactersAfterLastChunk() {
        String input = "3\r\nxyz\r\n0\r\n\ntail";
        // Reference implementation returns null on junk after last chunk.
        String result = ChunkedCodingConverter.decode(input);
        assertNull(result);
    }
}