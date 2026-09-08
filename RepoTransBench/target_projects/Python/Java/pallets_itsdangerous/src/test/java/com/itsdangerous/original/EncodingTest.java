package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.encoding.EncodingUtils;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class EncodingTest {

    @Test
    public void testWantBytesHandlesString() {
        String input = "foo";
        byte[] expected = input.getBytes(StandardCharsets.UTF_8);
        assertArrayEquals(expected, EncodingUtils.wantBytes(input));
    }

    @Test
    public void testWantBytesHandlesBytes() {
        byte[] input = new byte[] { 0x31, 0x32, 0x33 };
        assertArrayEquals(input, EncodingUtils.wantBytes(input));
    }

    @Test
    public void testBase64Encode() {
        String original = "hello";
        String encoded = EncodingUtils.base64Encode(EncodingUtils.wantBytes(original));
        // Re-encode python: base64.urlsafe_b64encode(b'hello').decode('utf-8').rstrip('=')
        assertEquals("aGVsbG8", encoded);
    }

    @Test
    public void testBase64Decode() {
        String encoded = "aGVsbG8";
        byte[] decoded = EncodingUtils.base64Decode(encoded);
        String expected = "hello";
        assertArrayEquals(expected.getBytes(StandardCharsets.UTF_8), decoded);
    }

    @Test
    public void testBase64DecodeMissingPadding() {
        // Should decode OK even with missing padding
        String encoded = "cHl0aG9u"; // "python"
        byte[] decoded = EncodingUtils.base64Decode(encoded);
        String expected = "python";
        assertArrayEquals(expected.getBytes(StandardCharsets.UTF_8), decoded);
    }

    @Test
    public void testBase64DecodeRaisesError() {
        assertThrows(Exception.class, () -> {
            EncodingUtils.base64Decode("!!@@", true);
        });
    }
}