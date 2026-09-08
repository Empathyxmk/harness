package com.peritus.bumpversion.original;

import com.peritus.bumpversion.versionpart.*;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class VersionPartTest {

    private VersionPartConfigFixture[] configs = new VersionPartConfigFixture[]{
            new VersionPartConfigFixture(new NumericVersionPartConfiguration()),
            new VersionPartConfigFixture(new ConfiguredVersionPartConfiguration(new String[]{"0", "1", "2"})),
            new VersionPartConfigFixture(new ConfiguredVersionPartConfiguration(new String[]{"0", "3"}))
    };

    @Test
    void testVersionPartInit() {
        for (VersionPartConfigFixture confvpc : configs) {
            assertEquals(confvpc.getFirstValue(),
                    new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()).getValue());
        }
    }

    @Test
    void testVersionPartCopy() {
        for (VersionPartConfigFixture confvpc : configs) {
            VersionPart vp = new VersionPart(confvpc.getFirstValue(), confvpc.getConfig());
            VersionPart vc = vp.copy();
            assertEquals(vp.getValue(), vc.getValue());
            assertNotSame(vp, vc);
        }
    }

    @Test
    void testVersionPartBump() {
        for (VersionPartConfigFixture confvpc : configs) {
            VersionPart vp = new VersionPart(confvpc.getFirstValue(), confvpc.getConfig());
            VersionPart vc = vp.bump();
            assertEquals(confvpc.getConfig().bump(confvpc.getFirstValue()), vc.getValue());
        }
    }

    @Test
    void testVersionPartCheckOptionalFalse() {
        for (VersionPartConfigFixture confvpc : configs) {
            assertFalse(new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()).bump().isOptional());
        }
    }

    @Test
    void testVersionPartCheckOptionalTrue() {
        for (VersionPartConfigFixture confvpc : configs) {
            assertTrue(new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()).isOptional());
        }
    }

    @Test
    void testVersionPartFormat() {
        for (VersionPartConfigFixture confvpc : configs) {
            String formatted = new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()).toString();
            assertEquals(confvpc.getFirstValue(), formatted);
        }
    }

    @Test
    void testVersionPartEquality() {
        for (VersionPartConfigFixture confvpc : configs) {
            assertEquals(new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()),
                         new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()));
        }
    }

    @Test
    void testVersionPartNull() {
        for (VersionPartConfigFixture confvpc : configs) {
            assertEquals(
                    new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()),
                    new VersionPart(confvpc.getFirstValue(), confvpc.getConfig()).nullVersion()
            );
        }
    }
}

// Dummy fixtures to adapt flexible configuration
class VersionPartConfigFixture {
    private final PartConfiguration config;
    public VersionPartConfigFixture(PartConfiguration config) {
        this.config = config;
    }
    public PartConfiguration getConfig() { return config; }
    public String getFirstValue() { return config.firstValue(); }
}