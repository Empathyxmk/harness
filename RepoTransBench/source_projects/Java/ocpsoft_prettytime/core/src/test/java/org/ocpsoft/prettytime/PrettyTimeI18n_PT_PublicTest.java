package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Portuguese, with different input than the original.
 */
public class PrettyTimeI18n_PT_PublicTest
{
    @Test
    public void testPortugueseSecondsAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("pt"));
        // 33 seconds ago
        Date past = new Date(System.currentTimeMillis() - 33L * 1000);
        String result = pt.format(past);
        assertTrue(result.toLowerCase().contains("segundo"));
        assertTrue(result.toLowerCase().contains("atrás"));
    }

    @Test
    public void testPortugueseInFutureDayPublic() {
        PrettyTime pt = new PrettyTime(new Locale("pt"));
        // 3 days from now
        Date future = new Date(System.currentTimeMillis() + 3L * 24 * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.toLowerCase().contains("em"));
        assertTrue(result.toLowerCase().contains("dia"));
    }
}