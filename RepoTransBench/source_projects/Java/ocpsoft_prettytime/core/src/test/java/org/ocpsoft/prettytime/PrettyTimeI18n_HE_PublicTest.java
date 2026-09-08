package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.*;

public class PrettyTimeI18n_HE_PublicTest {

    private static final Locale LOCALE = new Locale("he");

    @Test
    public void testPrettyTimeInHebrew_SecondsAhead() {
        PrettyTime p = new PrettyTime(new Date(0), LOCALE);
        String actual = p.format(new Date(4000));
        // Should expect "עוד ‏4 שניות" or similar, but avoid same as original test
        assertTrue(actual.contains("עוד"));
        assertTrue(actual.contains("שנ"));
        assertTrue(actual.contains("4") || actual.contains("ארבע"));
    }

    @Test
    public void testPrettyTimeInHebrew_MinutesBehind() {
        PrettyTime p = new PrettyTime(new Date(0), LOCALE);
        String actual = p.format(new Date(-6 * 60 * 1000));
        assertTrue(actual.contains("לפני"));
        assertTrue(actual.contains("6"));
        assertTrue(actual.contains("דק") || actual.contains("דקות"));
    }

    @Test
    public void testRightNow() {
        PrettyTime p = new PrettyTime(LOCALE);
        String actual = p.format(new Date());
        // "עכשיו" means "now" in Hebrew
        assertTrue(actual.contains("עכשיו"));
    }
}