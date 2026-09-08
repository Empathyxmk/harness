package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicInitSmokeTest {

    static class DummyApp {
        public java.util.Map<String,Object> config = new java.util.HashMap<>();
        public java.util.Map<String,Object> extensions = new java.util.HashMap<>();
    }

    @Test
    void testPublicBabelInitAndAppProperties() {
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
    void testPublicBabelInitAppConfigOptionsOverride() {
        DummyApp app = new DummyApp();
        app.config.put("BABEL_DEFAULT_LOCALE", "es");
        app.config.put("BABEL_DOMAIN", "alt_domain");
        app.config.put("BABEL_TRANSLATION_DIRECTORIES", "alpha;beta");
        Babel babel = new Babel();
        babel.initApp(app);
        BabelConfiguration config = (BabelConfiguration) app.extensions.get("babel");
        assertEquals("es", config.getDefaultLocale());
        assertEquals("alt_domain", config.getDefaultDomain());
        assertArrayEquals(new String[]{"alpha", "beta"}, config.getDefaultDirectories().toArray());
    }

    @Test
    void testPublicBabelInitAppWithSelectors() {
        DummyApp app = new DummyApp();
        Babel.LocaleSelector selector = () -> "it";
        Babel babel = new Babel();
        babel.initApp(app, selector, selector);
        BabelConfiguration config = (BabelConfiguration) app.extensions.get("babel");
        assertEquals("it", config.getLocaleSelector().select());
        assertEquals("it", config.getTimezoneSelector().select());
    }

    @Test
    void testPublicGetBabel() {
        DummyApp app = new DummyApp();
        Babel babel = new Babel();
        babel.initApp(app);
        BabelConfiguration config = Babel.getBabel(app);
        assertTrue(config instanceof BabelConfiguration);
        assertThrows(RuntimeException.class, Babel::getBabel);
    }

    @Test
    void testPublicDefaultDateFormatsDefined() {
        Babel b = new Babel();
        java.util.Map<String, String> d = b.getDefaultDateFormats();
        assertTrue(d instanceof java.util.Map<?,?>);
        assertEquals("medium", d.get("date"));
    }
}