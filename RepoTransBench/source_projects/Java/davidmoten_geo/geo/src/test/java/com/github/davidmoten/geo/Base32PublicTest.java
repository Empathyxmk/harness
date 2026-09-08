package com.github.davidmoten.geo;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class Base32PublicTest {

    @Test
    public void testEncodeBase32DifferentValue() {
        assertEquals("1y2p0ij32e8e", Base32.encodeBase32(1234567890123456L, 12));
    }

    @Test
    public void testDecodeBase32DifferentValue() {
        assertEquals(123456789L, Base32.decodeBase32("1ly7vk"));
    }

    @Test
    public void testPadLeftWithZerosToLengthPublic() {
        assertEquals("00000123", Base32.padLeftWithZerosToLength("123", 8));
    }

    @Test
    public void testGetCharIndexDifferentChar() {
        assertEquals(21, Base32.getCharIndex('q'));
    }

}