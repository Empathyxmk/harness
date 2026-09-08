package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicGettextTest {

    @Test
    void testPublicBasicTranslation() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, "ja");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String rv = b.gettext("Hi %(name)s!", "Taro");
            assertNotNull(rv);
            assertTrue(rv.contains("Taro"));
        }
    }

    @Test
    void testPublicNgettext() {
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
    void testPublicLazyGettext() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            LazyString lazyHello = b.lazyGettext("Welcome, %(guest)s!");
            String s = lazyHello.format(new Object[]{"Kenta"});
            assertTrue(s.contains("Kenta"));
        }
    }

    @Test
    void testPublicGettextWithDomain() {
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_DOMAIN", "myapp");
        Babel b = new Babel(app, "de_DE");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String val = b.gettext("Good night");
            assertNotNull(val);
            assertTrue(val.contains("Good"));
        }
    }
}