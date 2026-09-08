package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.example.shortuuid.*;

class ShortUUIDInitImportsTest {

    @Test
    void testAllNess() {
        String[] all = com.example.shortuuid.ShortUUIDStatic.ALL;
        for (String sym : all) {
            assertNotNull(com.example.shortuuid.ShortUUIDStatic.getSymbol(sym));
        }
    }

    @Test
    void testVersionPresent() {
        assertTrue(com.example.shortuuid.ShortUUIDStatic.VERSION instanceof String);
    }

    @Test
    void testDecodeAndEncodeAreSameAsMain() {
        assertSame(Main::encode, ShortUUIDStatic::encode);
        assertSame(Main::decode, ShortUUIDStatic::decode);
    }

    @Test
    void testGetSetAlphabetRespectsChanges() {
        String alpha1 = Main.getAlphabet();
        Main.setAlphabet("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz");
        String alpha2 = Main.getAlphabet();
        assertTrue(alpha2 instanceof String);
        assertNotEquals("", alpha2);
    }

    @Test
    void testRandomAndUuidAreCallable() {
        assertTrue(Main.random() instanceof String);
        assertTrue(Main.uuid() instanceof String);
    }

    @Test
    void testShortuuidClassIsAvailableAndWorks() {
        ShortUUID s = new ShortUUID();
        String u = s.uuid();
        assertTrue(u instanceof String);
    }
}