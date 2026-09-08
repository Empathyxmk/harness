package com.github.davidmoten.geo;

import org.junit.Test;
import static org.junit.Assert.*;

public class Base32Test {

    @Test
    public void testEncodeBase32LongPositive() {
        long l = 123456789L;
        String encoded = Base32.encodeBase32(l, 8);
        assertNotNull(encoded);
        assertEquals(8, encoded.length());
    }

    @Test
    public void testEncodeBase32LongNegative() {
        long l = -987654321L;
        String encoded = Base32.encodeBase32(l, 10);
        assertNotNull(encoded);
        assertTrue(encoded.startsWith("-"));
        assertEquals(11, encoded.length()); // "-" + 10 digits
    }

    @Test
    public void testEncodeBase32DefaultLength() {
        String encoded = Base32.encodeBase32(123);
        assertEquals(GeoHash.MAX_HASH_LENGTH, encoded.length());
    }

    @Test
    public void testDecodeBase32Positive() {
        long original = 123456789L;
        String encoded = Base32.encodeBase32(original, 12);
        long decoded = Base32.decodeBase32(encoded);
        assertEquals(original, decoded);
    }

    @Test
    public void testDecodeBase32Negative() {
        long original = -987654321L;
        String encoded = Base32.encodeBase32(original, 6);
        long decoded = Base32.decodeBase32(encoded);
        assertEquals(original, decoded);
    }

    @Test
    public void testGetCharIndexValid() {
        assertEquals(Integer.valueOf(1), Integer.valueOf(Base32.getCharIndex('1')));
        assertEquals(Integer.valueOf(10), Integer.valueOf(Base32.getCharIndex('b')));
        assertEquals(Integer.valueOf(31), Integer.valueOf(Base32.getCharIndex('z')));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetCharIndexInvalid() {
        Base32.getCharIndex('!');
    }

    @Test
    public void testPadLeftWithZerosToLengthShort() {
        String result = Base32.padLeftWithZerosToLength("abc", 5);
        assertEquals("00abc", result);
    }

    @Test
    public void testPadLeftWithZerosToLengthExact() {
        String result = Base32.padLeftWithZerosToLength("abc", 3);
        assertEquals("abc", result);
    }
}