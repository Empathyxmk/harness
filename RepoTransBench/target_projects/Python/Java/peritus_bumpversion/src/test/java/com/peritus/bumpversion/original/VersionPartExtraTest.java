package com.peritus.bumpversion.original;

import com.peritus.bumpversion.versionpart.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class VersionPartExtraTest {

    @Test
    void testVersionPartDefault() {
        VersionPart vp = new VersionPart("1");
        assertEquals("1", vp.getValue());
        assertFalse(vp.isOptional());
        assertEquals(vp, vp.copy());
        assertTrue(vp.toString() instanceof String);
        assertTrue(vp.toString().length() > 0);
        VersionPart vpBumped = vp.bump();
        assertEquals("2", vpBumped.getValue());
    }

    @Test
    void testVersionPartWithConfigured() {
        ConfiguredVersionPartConfiguration cfg = new ConfiguredVersionPartConfiguration(new String[]{"a", "b"});
        VersionPart vp = new VersionPart("a", cfg);
        assertEquals("a", vp.getValue());
        VersionPart vp2 = vp.bump();
        assertEquals("b", vp2.getValue());
    }

    @Test
    void testVersionPartNullAndEq() {
        NumericVersionPartConfiguration cfg = new NumericVersionPartConfiguration();
        VersionPart vp = new VersionPart("4", cfg);
        VersionPart nullVp = vp.nullVersion();
        assertEquals(cfg.firstValue(), nullVp.getValue());
        assertNotEquals(vp, nullVp);
        VersionPart vp2 = new VersionPart("4", cfg);
        assertEquals(vp, vp2);
    }

    @Test
    void testPartConfigProperties() {
        NumericVersionPartConfiguration cfg = new NumericVersionPartConfiguration();
        assertEquals("0", cfg.firstValue());
        assertEquals("0", cfg.optionalValue());
        assertEquals("10", cfg.bump("9"));
    }
}