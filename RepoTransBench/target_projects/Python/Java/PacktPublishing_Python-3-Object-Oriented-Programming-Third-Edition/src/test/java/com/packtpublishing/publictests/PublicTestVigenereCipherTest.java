package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for Vigenère cipher (from Chapter12/Case Study_ Vigenère cipher/test_vigenere.py).
 * Reimplements expected public test cases for the cipher's encode/decode methods.
 */
class PublicTestVigenereCipherTest {

    static String vigenereEncode(String plaintext, String key) {
        StringBuilder ciphertext = new StringBuilder();
        key = key.toUpperCase();
        int keyIndex = 0;
        for (char c : plaintext.toCharArray()) {
            if (Character.isLetter(c)) {
                char base = Character.isUpperCase(c) ? 'A' : 'a';
                char k = key.charAt(keyIndex % key.length());
                int kShift = k - 'A';
                int p = (c - base + kShift) % 26 + base;
                ciphertext.append((char)p);
                keyIndex++;
            } else {
                ciphertext.append(c);
            }
        }
        return ciphertext.toString();
    }

    static String vigenereDecode(String ciphertext, String key) {
        StringBuilder plaintext = new StringBuilder();
        key = key.toUpperCase();
        int keyIndex = 0;
        for (char c : ciphertext.toCharArray()) {
            if (Character.isLetter(c)) {
                char base = Character.isUpperCase(c) ? 'A' : 'a';
                char k = key.charAt(keyIndex % key.length());
                int kShift = k - 'A';
                int p = (c - base - kShift + 26) % 26 + base;
                plaintext.append((char)p);
                keyIndex++;
            } else {
                plaintext.append(c);
            }
        }
        return plaintext.toString();
    }

    @Test
    void testEncodeBasic() {
        // "attack at dawn", key "LEMON"
        String encoded = vigenereEncode("ATTACKATDAWN", "LEMON");
        assertEquals("LXFOPVEFRNHR", encoded);
    }

    @Test
    void testDecodeBasic() {
        String decoded = vigenereDecode("LXFOPVEFRNHR", "LEMON");
        assertEquals("ATTACKATDAWN", decoded);
    }

    @Test
    void testEncodeWithLowercase() {
        String encoded = vigenereEncode("attack at dusk!", "lemon");
        assertEquals("lxfopv ef rhzc!", encoded.toLowerCase());
    }

    @Test
    void testDecodeSentenceWithSpaces() {
        String enc = vigenereEncode("The cake is a lie", "abc");
        String dec = vigenereDecode(enc, "abc");
        assertEquals("The cake is a lie", dec);
    }

    @Test
    void testEncodeEmpty() {
        assertEquals("", vigenereEncode("", "lemon"));
    }

    @Test
    void testDecodeEmpty() {
        assertEquals("", vigenereDecode("", "lemon"));
    }

    @Test
    void testEncodeNonLetters() {
        assertEquals("123 !@#", vigenereEncode("123 !@#", "lemon"));
    }

    @Test
    void testDecodeNonLetters() {
        assertEquals("123 !@#", vigenereDecode("123 !@#", "lemon"));
    }
}