package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Russian, with new data.
 */
public class PrettyTimeI18n_RU_PublicTest
{
    @Test
    public void testRussianHoursAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("ru"));
        // 5 hours ago
        Date past = new Date(System.currentTimeMillis() - 5L * 60 * 60 * 1000);
        String result = pt.format(past);
        // In Russian, "назад" means "ago", "час" is "hour"
        assertTrue(result.contains("назад"));
        assertTrue(result.contains("час"));
    }

    @Test
    public void testRussianInFutureMinutesPublic() {
        PrettyTime pt = new PrettyTime(new Locale("ru"));
        // 16 minutes from now
        Date future = new Date(System.currentTimeMillis() + 16L * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.contains("через"));
        assertTrue(result.contains("мин"));
    }
}