package org.ocpsoft.prettytime;

import org.junit.Test;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.assertTrue;

/**
 * Public i18n test using Simplified Chinese, new test data.
 */
public class PrettyTimeI18n_ZH_CN_PublicTest
{
    @Test
    public void testChineseMinutesAgoPublic() {
        PrettyTime pt = new PrettyTime(Locale.SIMPLIFIED_CHINESE);
        // 45 minutes ago
        Date past = new Date(System.currentTimeMillis() - 45L * 60 * 1000);
        String result = pt.format(past);
        assertTrue(result.contains("分钟前"));
    }

    @Test
    public void testChineseInFutureDaysPublic() {
        PrettyTime pt = new PrettyTime(Locale.SIMPLIFIED_CHINESE);
        // 10 days from now
        Date future = new Date(System.currentTimeMillis() + 10L * 24 * 60 * 60 * 1000);
        String result = pt.format(future);
        assertTrue(result.contains("天后"));
    }
}