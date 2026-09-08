package com.jude.utils;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class JTimeTransformPublicTest {

    @Test
    void testDefaultConstructorPublic() {
        JTimeTransform jtt = new JTimeTransform();
        assertNotNull(jtt);
        assertTrue(jtt.getYear() > 2010 && jtt.getYear() < 2100); // plausible year range (less restrictive)
        assertTrue(jtt.getMonth() >= 1 && jtt.getMonth() <= 12);
        assertTrue(jtt.getDay() >= 1 && jtt.getDay() <= 31);
        assertTrue(jtt.getTimestamp() > 0);
    }

    @Test
    void testLongConstructorPublic() {
        long fiveDaysAgo = (System.currentTimeMillis() / 1000) - 432000;
        JTimeTransform jtt = new JTimeTransform(fiveDaysAgo);
        assertEquals(fiveDaysAgo, jtt.getTimestamp(), 2); // Allow for rounding difference
    }

    @Test
    void testYMDConstructorPublic() {
        JTimeTransform jtt = new JTimeTransform(2021, 10, 11); // Nov 11, 2021
        assertEquals(2021, jtt.getYear());
        assertEquals(11, jtt.getMonth());
        assertEquals(11, jtt.getDay());
    }

    @Test
    void testToStringFormatPublic() {
        JTimeTransform jtt = new JTimeTransform(2020, 6, 4); // July 4, 2020
        String str = jtt.toString("yyyy/MM/dd");
        assertTrue(str.startsWith("2020/07/04"));
    }

    @Test
    void testParseSuccessPublic() {
        JTimeTransform jtt = new JTimeTransform(2019, 4, 15); // May 15, 2019
        JTimeTransform result = jtt.parse("yyyy/MM/dd", "2019/06/01");
        assertNotNull(result);
        assertEquals(2019, result.getYear());
        assertEquals(6, result.getMonth());
        assertEquals(1, result.getDay());
    }

    @Test
    void testParseFailurePublic() {
        JTimeTransform jtt = new JTimeTransform(2018, 1, 5);
        JTimeTransform result = jtt.parse("yyyy/MM/dd", "notadate");
        assertNull(result);
    }

    @Test
    void testRecentDateFormatPublic() {
        long now = System.currentTimeMillis() / 1000;
        JTimeTransform justNow = new JTimeTransform(now);
        JTimeTransform twoMinAgo = new JTimeTransform(now - 120);
        JTimeTransform threeHourAgo = new JTimeTransform(now - 3 * 3600);
        JTimeTransform twoDaysAgo = new JTimeTransform(now - 2 * 86400);
        JTimeTransform twoDaysLater = new JTimeTransform(now + 2 * 86400);

        JTimeTransform.RecentDateFormat rdf = new JTimeTransform.RecentDateFormat("yyyy/MM/dd");

        String secText = rdf.format(new JTimeTransform(now-2), 2);
        assertTrue(secText.contains("秒前") || secText.contains("秒"));

        String minText = rdf.format(twoMinAgo, 120);
        assertTrue(minText.contains("分钟前"));

        String hourText = rdf.format(threeHourAgo, 3 * 3600);
        assertTrue(hourText.contains("小时前"));

        String dtText = twoMinAgo.toString(rdf);
        assertNotNull(dtText);

        // Future times
        String futureSec = rdf.format(new JTimeTransform(now+3), -3);
        assertTrue(futureSec.contains("秒后") || futureSec.contains("秒"));

        String futureDay = rdf.format(new JTimeTransform(now+3600*50), -3600*50);
        assertTrue(futureDay.contains("天后") || futureDay.contains("天"));

        String fallbackPast = rdf.format(twoDaysAgo, 2 * 86400);
        assertNotNull(fallbackPast);

        String fallbackFuture = rdf.format(twoDaysLater, -2 * 86400);
        assertNotNull(fallbackFuture);
    }
}