package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicAppFactoryTest {

    @Test
    void testPublicBabelWithAppFactory() {
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_DEFAULT_LOCALE", "es");
        Babel b = new Babel(app);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("es", b.getLocale().toString());
        }
    }

    @Test
    void testPublicBabelFactoryDeferredInit() {
        java.util.List<Integer> created = new java.util.ArrayList<>();
        Babel.LocaleSelector selector = () -> { created.add(100); return "fr"; };
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        b.initApp(app, selector, null);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("fr", b.getLocale().toString());
            assertEquals(1, created.size());
        }
    }
}