package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Japanese, new test data.
 */
public class PrettyTimeI18n_JA_PublicTest
{
    @Test
    public void testJapaneseMinutesAgoPublic() {
        PrettyTime pt = new PrettyTime(new Locale("ja"));
        // 15 minutes ago
        Date past = new Date(System.currentTimeMillis() - 15L * 60 * 1000);
        String result = pt.format(past);
        assertTrue(result.contains("分前"));
    }

    @Test
    public void testJapaneseFromNowHourPublic() {
        PrettyTime pt = new PrettyTime(new Locale("ja"));
        // 1 hour from now
        Date future = new Date(System.currentTimeMillis() + 60L * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.contains("1時間後") || result.contains("時間後"));
    }
}