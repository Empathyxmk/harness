package com.peritus.bumpversion.publictests;

import com.peritus.bumpversion.versionpart.VersionPart;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicVersionPartExtraTest {

    @Test
    void testPublicVersionPartHasValue() {
        VersionPart vp = new VersionPart("nonempty", null, null);
        assertTrue(vp.hasValue());
    }

    @Test
    void testPublicVersionPartNotHasValueEmptyString() {
        VersionPart vp = new VersionPart("", null, null);
        assertFalse(vp.hasValue());
    }

    @Test
    void testPublicVersionPartIntCastZero() {
        VersionPart vp = new VersionPart("0", null, null);
        assertEquals(0, vp.toInt());
    }

    @Test
    void testPublicVersionPartIgnoreValue() {
        VersionPart vp = new VersionPart("ignored", null, null);
        assertEquals("ignored", vp.getValue());
    }

    @Test
    void testPublicVersionPartReprContainsClass() {
        VersionPart vp = new VersionPart("classy", null, null);
        assertTrue(vp.toString().contains("VersionPart"));
    }
}