package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using French, with test data different from the original.
 */
public class PrettyTimeI18n_FR_PublicTest
{
    @Test
    public void testFrenchMinutesAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("fr"));
        // 20 minutes ago
        Date tenMinutesAgo = new Date(System.currentTimeMillis() - 20L * 60 * 1000);
        String result = pt.format(tenMinutesAgo);
        assertTrue(result.toLowerCase().contains("il y a"));
        assertTrue(result.toLowerCase().contains("minutes"));
    }

    @Test
    public void testFrenchInFutureHoursPublic() {
        PrettyTime pt = new PrettyTime(new Locale("fr"));
        // 4 hours from now
        Date future = new Date(System.currentTimeMillis() + 4L * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.toLowerCase().contains("dans"));
        assertTrue(result.toLowerCase().contains("heures"));
    }
}