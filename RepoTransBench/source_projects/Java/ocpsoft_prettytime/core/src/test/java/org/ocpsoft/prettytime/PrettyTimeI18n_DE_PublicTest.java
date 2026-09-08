package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using German, new test data.
 */
public class PrettyTimeI18n_DE_PublicTest
{
    @Test
    public void testGermanSecondsAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("de"));
        // 9 seconds ago
        Date past = new Date(System.currentTimeMillis() - 9L * 1000);
        String result = pt.format(past);
        assertTrue(result.toLowerCase().contains("vor"));
        assertTrue(result.toLowerCase().contains("sekunden"));
    }

    @Test
    public void testGermanInYearFuturePublic() {
        PrettyTime pt = new PrettyTime(new Locale("de"));
        // 1 year from now
        Date future = new Date(System.currentTimeMillis() + 365L * 24 * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.toLowerCase().contains("in"));
        assertTrue(result.toLowerCase().contains("jahr") || result.toLowerCase().contains("jahren"));
    }
}