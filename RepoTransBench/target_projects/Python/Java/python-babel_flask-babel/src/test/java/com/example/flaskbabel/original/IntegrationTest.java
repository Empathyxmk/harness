package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class IntegrationTest {

    @Test
    void testNoRequestContext() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        b.initApp(app);

        try (DummyAppContext ctx = app.appContext()) {
            assertTrue(b.getTranslations() instanceof NullTranslations);
        }
    }

    @Test
    void testMultipleDirectories() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations;renamed_translations");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(4, translations.length);
            assertEquals("de", translations[0].toString());
            assertEquals("ja", translations[1].toString());
            assertEquals("de", translations[2].toString());
            assertEquals("de_DE", translations[3].toString());
            assertEquals("Hallo Peter!", b.gettext("Hello %(name)s!", "Peter"));
        }
    }

    @Test
    void testMultipleDirectoriesMultipleDomains() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "renamed_translations;translations_different_domain");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "messages;myapp");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(3, translations.length);
            assertEquals("de", translations[0].toString());
            assertEquals("de", translations[1].toString());
            assertEquals("de_DE", translations[2].toString());
            assertEquals("Hallo Peter!", b.gettext("Hello %(name)s!", "Peter"));
            assertEquals("Auf Wiedersehen", b.gettext("Good bye"));
        }
    }

    @Test
    void testMultipleDirectoriesDifferentDomain() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations_different_domain;renamed_translations");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "myapp");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(3, translations.length);
            assertEquals("de", translations[0].toString());
            assertEquals("de", translations[1].toString());
            assertEquals("de_DE", translations[2].toString());
            assertEquals("Hallo Peter!", b.gettext("Hello %(name)s!", "Peter"));
            assertEquals("Auf Wiedersehen", b.gettext("Good bye"));
        }
    }

    @Test
    void testDifferentDomain() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations_different_domain");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "myapp");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(2, translations.length);
            assertEquals("de", translations[0].toString());
            assertEquals("de_DE", translations[1].toString());
            assertEquals("Auf Wiedersehen", b.gettext("Good bye"));
        }
    }

    @Test
    void testLazyOldStyleFormatting() {
        LazyString lazyString = Babel.lazyGettext("Hello %(name)s");
        assertEquals("Hello test", lazyString.format(new Object[]{"test"}));

        lazyString = Babel.lazyGettext("test");
        assertEquals("Hello test", String.format("Hello %s", lazyString));
    }

    @Test
    void testLazyPickling() throws Exception {
        LazyString lazyString = Babel.lazyGettext("Foo");

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(lazyString);
        oos.close();

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        LazyString unpickled = (LazyString) ois.readObject();
        assertEquals(lazyString, unpickled);
    }
}