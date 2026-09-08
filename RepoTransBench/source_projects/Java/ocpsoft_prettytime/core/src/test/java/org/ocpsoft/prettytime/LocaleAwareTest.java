package org.ocpsoft.prettytime;

import org.junit.jupiter.api.Test;
import java.util.Locale;
import static org.junit.jupiter.api.Assertions.*;

class LocaleAwareTest {

    static class DummyLocaleAware implements LocaleAware<DummyLocaleAware> {
        private Locale locale;
        @Override
        public DummyLocaleAware setLocale(Locale locale) {
            this.locale = locale;
            return this;
        }
        Locale getLocale() { return locale; }
    }

    @Test
    void testSetLocale() {
        DummyLocaleAware aware = new DummyLocaleAware();
        Locale l = Locale.FRENCH;
        DummyLocaleAware ret = aware.setLocale(l);
        assertSame(aware, ret);
        assertEquals(Locale.FRENCH, aware.getLocale());
    }
}