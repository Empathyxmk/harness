package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Spanish, new test data.
 */
public class PrettyTimeI18n_ES_PublicTest
{
    @Test
    public void testSpanishMinutesAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("es"));
        // 29 minutes ago
        Date past = new Date(System.currentTimeMillis() - 29L * 60 * 1000);
        String result = pt.format(past);
        assertTrue(result.toLowerCase().contains("hace"));
        assertTrue(result.toLowerCase().contains("minuto"));
    }

    @Test
    public void testSpanishInYearFuturePublic() {
        PrettyTime pt = new PrettyTime(new Locale("es"));
        // 2 years from now
        Date future = new Date(System.currentTimeMillis() + 2L * 365 * 24 * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.toLowerCase().contains("dentro de"));
        assertTrue(result.toLowerCase().contains("año"));
    }
}