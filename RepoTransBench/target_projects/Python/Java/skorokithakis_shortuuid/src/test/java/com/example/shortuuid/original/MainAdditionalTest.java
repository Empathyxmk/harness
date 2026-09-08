package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.example.shortuuid.Main;
import com.example.shortuuid.ShortUUID;

import java.util.List;
import java.util.UUID;

class MainAdditionalTest {

    @Test
    void testIntToStringAndStringToIntIdentity() {
        String alphabet = "abcdef1234";
        List<Character> alpha = alphabet.chars().mapToObj(e -> (char) e).toList();
        long[] nums = {0, 1, 10, 123456789, (1L<<64)};
        for (long num : nums) {
            String s = Main.intToString(num, alpha, 8);
            long restored = Main.stringToInt(s, alpha);
            assertEquals(num, restored);
        }
    }

    @Test
    void testEncodeAndDecodeRoundtrip() {
        UUID u = UUID.randomUUID();
        String s = Main.encode(u);
        UUID u2 = Main.decode(s);
        assertEquals(u, u2);
    }

    @Test
    void testGetAndSetAlphabet() {
        String alphabet = "zyxwvutsrqponmlkjihgfedcba234567";
        Main.setAlphabet(alphabet);
        String gotten = Main.getAlphabet();
        char[] arr1 = gotten.toCharArray();
        char[] arr2 = alphabet.toCharArray();
        java.util.Arrays.sort(arr1);
        java.util.Arrays.sort(arr2);
        assertArrayEquals(arr1, arr2);
    }

    @Test
    void testRandomLength() {
        String rand = Main.random(5);
        assertNotNull(rand);
        assertEquals(5, rand.length());
    }

    @Test
    void testSetAlphabetInvalid() {
        ShortUUID s = new ShortUUID();
        assertThrows(IllegalArgumentException.class, () -> {
            s.setAlphabet("a", false);
        });
    }

    @Test
    void testShortuuidEncodeUuidTypeError() {
        ShortUUID shortuuid = new ShortUUID();
        assertThrows(IllegalArgumentException.class, () -> shortuuid.encode("notauuid"));
    }

    @Test
    void testShortuuidDecodeStrTypeError() {
        ShortUUID shortuuid = new ShortUUID();
        assertThrows(IllegalArgumentException.class, () -> shortuuid.decode(12345));
    }

    @Test
    void testShortuuidPropertiesAndMethods() {
        ShortUUID shortuuid = new ShortUUID();
        assertTrue(shortuuid.length() > 0);
        assertNotNull(shortuuid.getAlphabet());
    }

    @Test
    void testShortuuidUuidRandomAndNamed() {
        ShortUUID shortuuid = new ShortUUID();
        String anon = shortuuid.uuid();
        assertNotNull(anon);
        String urlId = shortuuid.uuid("https://example.com");
        assertNotNull(urlId);
        String dnsId = shortuuid.uuid("myname");
        assertNotNull(dnsId);
    }

    @Test
    void testShortuuidRandomMethod() {
        ShortUUID shortuuid = new ShortUUID();
        String result = shortuuid.random(6);
        assertNotNull(result);
        assertEquals(6, result.length());
    }

    @Test
    void testDecodeLegacyBehavior() {
        UUID u = UUID.randomUUID();
        String s = Main.encode(u);
        String reversed = new StringBuilder(s).reverse().toString();
        UUID u2 = Main.decode(reversed, true);
        assertNotNull(u2);
    }

    @Test
    void testStringToIntInvalidChar() {
        List<Character> alpha = "abc".chars().mapToObj(e -> (char) e).toList();
        assertThrows(IllegalArgumentException.class, () -> Main.stringToInt("ad", alpha));
    }

    @Test
    void testIntToStringWithPadding() {
        List<Character> alpha = "abcde12345".chars().mapToObj(e -> (char) e).toList();
        String s = Main.intToString(5, alpha, 8);
        assertEquals(8, s.length());
    }

    @Test
    void testShortuuidSetAlphabetDontSort() {
        ShortUUID s = new ShortUUID("cba", true);
        assertEquals("cba", s.getAlphabet());
    }
}