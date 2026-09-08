package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GettextTest {

    @Test
    void testBasicTranslation() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, "de_DE");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String rv = b.gettext("Hello %(name)s!", "Johann");
            assertNotNull(rv);
            assertTrue(rv.contains("Johann"));
        }
    }

    @Test
    void testNgettext() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, "de_DE");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String rvSing = b.ngettext("There is %(num)d mouse", "There are %(num)d mice", 1);
            assertTrue(rvSing.contains("mouse"));
            String rvPlur = b.ngettext("There is %(num)d mouse", "There are %(num)d mice", 5);
            assertTrue(rvPlur.contains("mice"));
        }
    }

    @Test
    void testLazyGettext() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            LazyString lazyHello = b.lazyGettext("Welcome, %(guest)s!");
            String s = lazyHello.format(new Object[]{"Hans"});
            assertTrue(s.contains("Hans"));
        }
    }

    @Test
    void testGettextWithDomain() {
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_DOMAIN", "myapp");
        Babel b = new Babel(app, "de_DE");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String val = b.gettext("Good night");
            assertNotNull(val);
            assertTrue(val.contains("Good") || val.contains("Gute")); // Accept translated form
        }
    }
}