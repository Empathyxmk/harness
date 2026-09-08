package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicMultipleAppsTest {

    @Test
    void testPublicMultipleAppsLocales() {
        DummyFlaskApp app1 = new DummyFlaskApp();
        DummyFlaskApp app2 = new DummyFlaskApp();
        Babel b1 = new Babel(app1, "fr_FR");
        Babel b2 = new Babel(app2, "ja_JP");

        try (DummyRequestContext ctx1 = app1.testRequestContext()) {
            assertEquals("fr_FR", b1.getLocale().toString());
        }
        try (DummyRequestContext ctx2 = app2.testRequestContext()) {
            assertEquals("ja_JP", b2.getLocale().toString());
        }
    }
}