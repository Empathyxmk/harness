package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

class PublicIntegrationTest {

    @Test
    void testPublicNoRequestContext() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        b.initApp(app);

        try (DummyAppContext ctx = app.appContext()) {
            assertTrue(b.getTranslations() instanceof NullTranslations);
        }
    }

    @Test
    void testPublicMultipleDirectories() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations;renamed_translations");
        app.setConfig("BABEL_DEFAULT_LOCALE", "ja");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertTrue(translations.length == 3 || translations.length == 4);
            assertTrue(translations[0].toString().equals("de") || translations[0].toString().equals("ja"));
            assertEquals("Good morning, Anna!", b.gettext("Good morning, %(who)s!", "Anna"));
        }
    }

    @Test
    void testPublicMultipleDirectoriesMultipleDomains() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "renamed_translations;translations_different_domain");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "myapp;messages");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(3, translations.length);
            assertEquals("de", translations[1].toString());
            assertEquals("Thank you", b.gettext("Thank you"));
            assertEquals("See you", b.gettext("See you"));
        }
    }

    @Test
    void testPublicMultipleDirectoriesDifferentDomain() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations_different_domain;renamed_translations");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "myapp");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(3, translations.length);
            assertEquals("de_DE", translations[2].toString());
            assertEquals("Farewell", b.gettext("Farewell"));
            assertEquals("Bonjour", b.gettext("Bonjour"));
        }
    }

    @Test
    void testPublicDifferentDomain() {
        Babel b = new Babel();
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_TRANSLATION_DIRECTORIES", "translations_different_domain");
        app.setConfig("BABEL_DEFAULT_LOCALE", "de_DE");
        app.setConfig("BABEL_DOMAIN", "myapp");
        b.initApp(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            Translation[] translations = b.listTranslations();
            assertEquals(2, translations.length);
            assertEquals("de_DE", translations[1].toString());
            assertEquals("Salut", b.gettext("Salut"));
        }
    }

    @Test
    void testPublicLazyOldStyleFormatting() {
        LazyString lazyString = Babel.lazyGettext("Good morning, %(user)s");
        assertEquals("Good morning, Sophie", lazyString.format(new Object[]{"Sophie"}));
        lazyString = Babel.lazyGettext("bonjour");
        assertEquals("Good day: bonjour", String.format("Good day: %s", lazyString));
    }

    @Test
    void testPublicLazyPickling() throws Exception {
        LazyString lazyString = Babel.lazyGettext("Bar");

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(lazyString);
        oos.close();

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        LazyString unpickled = (LazyString)ois.readObject();

        assertEquals(lazyString, unpickled);
    }
}