package com.peritus.bumpversion.publictests;

import com.peritus.bumpversion.versionpart.VersionPart;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicVersionPartTest {

    @Test
    void testPublicVersionPartValueSetting() {
        VersionPart vp = new VersionPart("7", null, null);
        assertEquals("7", vp.toString());
    }

    @Test
    void testPublicVersionPartCompareDifferentValues() {
        VersionPart vp1 = new VersionPart("3", null, null);
        VersionPart vp2 = new VersionPart("10", null, null);
        assertNotEquals(vp1, vp2);
    }

    @Test
    void testPublicVersionPartEqualityWithSameValue() {
        VersionPart vp1 = new VersionPart("hello", null, null);
        VersionPart vp2 = new VersionPart("hello", null, null);
        assertEquals(vp1, vp2);
    }

    @Test
    void testPublicVersionPartRepr() {
        VersionPart vp = new VersionPart("2024", null, null);
        assertTrue(vp.toString().contains("2024"));
    }

    @Test
    void testPublicVersionPartStrCast() {
        VersionPart vp = new VersionPart("543", null, null);
        assertEquals("543", vp.toString());
    }

    @Test
    void testPublicVersionPartIntCast() {
        VersionPart vp = new VersionPart("8", null, null);
        assertEquals(8, vp.toInt());
    }

    @Test
    void testPublicVersionPartIntCastNonNumeric() {
        VersionPart vp = new VersionPart("xyz", null, null);
        assertThrows(NumberFormatException.class, vp::toInt);
    }
}