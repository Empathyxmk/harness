package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicForceLocaleTest {

    @Test
    void testPublicForceLocaleEng() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "en");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("en", b.getLocale().toString());
            try (ForceLocaleContext ignored = b.forceLocale("fr")) {
                assertEquals("fr", b.getLocale().toString());
            }
            assertEquals("en", b.getLocale().toString());
        }
    }

    @Test
    void testPublicForceLocaleChain() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "fr");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("fr", b.getLocale().toString());
            try (ForceLocaleContext ignored = b.forceLocale("ru")) {
                assertEquals("ru", b.getLocale().toString());
                try (ForceLocaleContext ignored2 = b.forceLocale("es")) {
                    assertEquals("es", b.getLocale().toString());
                }
                assertEquals("ru", b.getLocale().toString());
            }
            assertEquals("fr", b.getLocale().toString());
        }
    }
}