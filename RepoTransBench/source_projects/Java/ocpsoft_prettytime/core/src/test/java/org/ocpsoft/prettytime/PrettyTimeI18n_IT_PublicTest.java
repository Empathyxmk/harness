package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Italian, with different input than the original.
 */
public class PrettyTimeI18n_IT_PublicTest
{
    @Test
    public void testItalianDaysAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("it"));
        // 10 days ago
        Date past = new Date(System.currentTimeMillis() - 10L * 24 * 60 * 60 * 1000);
        String result = pt.format(past);
        assertTrue(result.toLowerCase().contains("fa"));
        assertTrue(result.toLowerCase().contains("giorni"));
    }

    @Test
    public void testItalianInFutureWeeksPublic() {
        PrettyTime pt = new PrettyTime(new Locale("it"));
        // 2 weeks from now
        Date future = new Date(System.currentTimeMillis() + 2L * 7 * 24 * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.toLowerCase().contains("tra"));
        assertTrue(result.toLowerCase().contains("settimane"));
    }
}