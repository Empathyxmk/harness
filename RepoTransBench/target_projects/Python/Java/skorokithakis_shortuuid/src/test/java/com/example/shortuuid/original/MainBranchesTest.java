package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.example.shortuuid.ShortUUID;
import com.example.shortuuid.Main;

import java.util.List;
import java.util.UUID;

class MainBranchesTest {

    @Test
    void testIntToStringZeroAndEmpty() {
        List<Character> alphabet = "abcd".chars().mapToObj(e -> (char) e).toList();
        assertEquals("aaaaa", Main.intToString(0, alphabet, 5));
    }

    @Test
    void testIntToStringShortPadding() {
        List<Character> alphabet = "abc".chars().mapToObj(e -> (char) e).toList();
        assertEquals("c", Main.intToString(2, alphabet, 1));
    }

    @Test
    void testDecodeLegacyTrueBehavior() {
        ShortUUID s = new ShortUUID();
        UUID u = UUID.randomUUID();
        String enc = s.encode(u);
        String rev = new StringBuilder(enc).reverse().toString();
        UUID u2 = s.decode(rev, true);
        assertNotNull(u2);
    }

    @Test
    void testSetAlphabetDontSortPreservedOrder() {
        ShortUUID s = new ShortUUID("ACBXYZ", true);
        assertEquals("ACBXYZ", s.getAlphabet());
    }

    @Test
    void testSetAlphabetErrors() {
        ShortUUID s = new ShortUUID();
        assertThrows(IllegalArgumentException.class, () -> s.setAlphabet("z", true));
        assertThrows(IllegalArgumentException.class, () -> s.setAlphabet("", true));
    }
}