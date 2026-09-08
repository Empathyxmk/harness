package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.example.shortuuid.Main;
import com.example.shortuuid.ShortUUID;

import java.util.UUID;

class ShortUUIDTest {

    @Test
    void testEncodingAndDecodingWithDefaultAlphabet() {
        UUID u = UUID.randomUUID();
        ShortUUID s = new ShortUUID();
        String code = s.encode(u);
        assertEquals(u, s.decode(code));
        String code2 = Main.encode(u);
        assertEquals(u, Main.decode(code2));
    }

    @Test
    void testEncodingAndDecodingCustomAlphabet() {
        String alphabet = "abcdefghijklmnopqrstuvw12345";
        ShortUUID s = new ShortUUID(alphabet);
        UUID u = UUID.randomUUID();
        String code = s.encode(u);
        assertEquals(u, s.decode(code));
    }

    @Test
    void testInvalidDecodeRaises() {
        assertThrows(Exception.class, () -> Main.decode("!!!notvalid!!!"));
    }

    @Test
    void testRoundtrip() {
        ShortUUID s = new ShortUUID();
        UUID u = UUID.randomUUID();
        String shortid = s.encode(u);
        assertEquals(u, s.decode(shortid));
    }

    @Test
    void testAlphabetSetterAndGetter() {
        ShortUUID s = new ShortUUID();
        String oldAlpha = s.getAlphabet();
        String customAlpha = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz";
        s.setAlphabet(customAlpha);
        String newAlpha = s.getAlphabet();
        assertEquals(newAlpha, String.join("", s._alphabetArray()));
        String reallyCustom = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNPQRSTUVWXYZ";
        s.setAlphabet(reallyCustom);
        assertNotEquals(oldAlpha, s.getAlphabet());
        ShortUUID s2 = new ShortUUID(true);
        String originalAlpha = "ZYXWVUTSRQPONMLKJHGFEDCBAabcdefghijkmnopqrstuvwxyz23456789";
        s2.setAlphabet(originalAlpha, true);
        assertEquals(originalAlpha, s2.getAlphabet());
    }

    @Test
    void testSetAlphabetPreservesCustom() {
        ShortUUID s = new ShortUUID("ciao", true);
        assertEquals("ciao", s.getAlphabet());
    }

    @Test
    void testUuidArgumentStrTypeRaises() {
        ShortUUID s = new ShortUUID();
        String uStr = UUID.randomUUID().toString();
        assertThrows(IllegalArgumentException.class, () -> s.encode(uStr));
    }

    @Test
    void testLegacyDefaultAlphabet() {
        ShortUUID s = new ShortUUID();
        UUID u = UUID.randomUUID();
        String enc = s.encode(u);
        UUID dec = s.decode(enc);
        assertEquals(u, dec);
    }

    @Test
    void testDecodeInvalidType() {
        ShortUUID s = new ShortUUID();
        assertThrows(Exception.class, () -> s.decode(12345));
    }
}