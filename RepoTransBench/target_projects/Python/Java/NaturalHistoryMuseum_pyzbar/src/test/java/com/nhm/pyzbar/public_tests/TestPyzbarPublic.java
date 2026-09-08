package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.pyzbar.ZBarSymbol;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPyzbarPublic {
    @Test
    void testEnumValues() {
        try {
            assertNotNull(ZBarSymbol.valueOf("CODE39"));
        } catch (IllegalArgumentException ignored) {
            fail("ZBarSymbol must define CODE39");
        }
        assertTrue(ZBarSymbol.CODE39 instanceof ZBarSymbol);
    }

    @Test
    void testAllSymbolsIncludesSymbol() {
        assertTrue(
                java.util.EnumSet.allOf(ZBarSymbol.class).contains(ZBarSymbol.CODE93),
                "ZBarSymbol.ALL must include CODE93"
        );
    }
}