package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.encoding.EncodingUtils;
import java.nio.charset.StandardCharsets;

public class EncodingPublicTest {

    @Test
    public void testWantBytesHandlesString() {
        String input = "foo";
        byte[] expected = input.getBytes(StandardCharsets.UTF_8);
        assertArrayEquals(expected, EncodingUtils.wantBytes(input));
    }

    @Test
    public void testBase64EncodeDecode() {
        String input = "bar";
        String encoded = EncodingUtils.base64Encode(input.getBytes(StandardCharsets.UTF_8));
        byte[] decoded = EncodingUtils.base64Decode(encoded);
        assertEquals(input, new String(decoded, StandardCharsets.UTF_8));
    }
}