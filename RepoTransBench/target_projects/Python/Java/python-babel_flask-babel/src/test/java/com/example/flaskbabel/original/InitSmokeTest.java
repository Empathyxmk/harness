package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class InitSmokeTest {

    static class DummyApp {
        public java.util.Map<String, Object> config = new java.util.HashMap<>();
        public java.util.Map<String, Object> extensions = new java.util.HashMap<>();
    }

    @Test
    void testBabelInitAndAppProperties() {
        DummyApp app = new DummyApp();
        Babel babel = new Babel();
        babel.initApp(app);
        Object config = app.extensions.get("babel");
        assertTrue(config instanceof BabelConfiguration);
        BabelConfiguration conf = (BabelConfiguration) config;
        assertEquals("en", conf.getDefaultLocale());
        assertEquals("messages", conf.getDefaultDomain());
        assertTrue(conf.getTranslationDirectories() instanceof java.util.List<?>);
        assertSame(babel, conf.getInstance());
    }

    @Test
    void testBabelInitAppConfigOptionsOverride() {
        DummyApp app = new DummyApp();
        app.config.put("BABEL_DEFAULT_LOCALE", "fr");
        app.config.put("BABEL_DOMAIN", "customdomain");
        app.config.put("BABEL_TRANSLATION_DIRECTORIES", "foo;bar");
        Babel babel = new Babel();
        babel.initApp(app);
        BabelConfiguration config = (BabelConfiguration) app.extensions.get("babel");
        assertEquals("fr", config.getDefaultLocale());
        assertEquals("customdomain", config.getDefaultDomain());
        assertArrayEquals(new String[]{"foo", "bar"}, config.getDefaultDirectories().toArray());
    }

    @Test
    void testBabelInitAppWithSelectors() {
        DummyApp app = new DummyApp();
        LocaleSelector selector = () -> "de";
        Babel babel = new Babel();
        babel.initApp(app, selector, selector);
        BabelConfiguration config = (BabelConfiguration) app.extensions.get("babel");
        assertEquals("de", config.getLocaleSelector().select());
        assertEquals("de", config.getTimezoneSelector().select());
    }

    @Test
    void testGetBabel() {
        DummyApp app = new DummyApp();
        Babel babel = new Babel();
        babel.initApp(app);
        BabelConfiguration config = Babel.getBabel(app);
        assertTrue(config instanceof BabelConfiguration);
        // fallback to current_app: should raise when current_app not set
        assertThrows(RuntimeException.class, Babel::getBabel);
    }

    @Test
    void testDefaultDateFormatsDefined() {
        Babel b = new Babel();
        java.util.Map<String, String> d = b.getDefaultDateFormats();
        assertTrue(d instanceof java.util.Map<?,?>);
        assertEquals("medium", d.get("datetime"));
    }
    // Dummy interfaces to support the tests
    interface LocaleSelector { String select(); }
}