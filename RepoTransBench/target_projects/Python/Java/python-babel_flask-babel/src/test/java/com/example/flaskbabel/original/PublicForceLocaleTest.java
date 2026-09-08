package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicForceLocaleTest {

    @Test
    void testPublicForceLocale() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "it");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("it", b.getLocale().toString());
            try (ForceLocaleContext ignored = b.forceLocale("es")) {
                assertEquals("es", b.getLocale().toString());
            }
            assertEquals("it", b.getLocale().toString());
        }
    }

    @Test
    void testPublicForceLocaleSetback() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "fr");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("fr", b.getLocale().toString());
            try (ForceLocaleContext ignored = b.forceLocale("ja")) {
                assertEquals("ja", b.getLocale().toString());
                try (ForceLocaleContext ignored2 = b.forceLocale("en")) {
                    assertEquals("en", b.getLocale().toString());
                }
                assertEquals("ja", b.getLocale().toString());
            }
            assertEquals("fr", b.getLocale().toString());
        }
    }
}