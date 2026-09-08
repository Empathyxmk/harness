package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppFactoryTest {

    @Test
    void testAppFactory() {
        Babel b = new Babel();

        LocaleSelector localeSelector = () -> "de_DE";

        DummyFlaskApp app = new DummyFlaskApp();
        b.initApp(app, "en_US", localeSelector);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("de_DE", b.getLocale().toString());
            assertEquals("Hallo Peter!", b.gettext("Hello %(name)s!", "Peter"));
        }
    }

    // Dummy interface to mimic locale selector lambda
    public interface LocaleSelector {
        String select();
    }
}