package com.jude.utils;

import org.junit.jupiter.api.Test;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

class JTimeTransformTest {

    @Test
    void testDefaultConstructor() {
        JTimeTransform jtt = new JTimeTransform();
        assertNotNull(jtt);
        assertTrue(jtt.getYear() > 2000); // should be a plausible year
        assertTrue(jtt.getMonth() > 0 && jtt.getMonth() < 13);
        assertTrue(jtt.getDay() > 0 && jtt.getDay() < 32);
        assertTrue(jtt.getTimestamp() > 0);
    }

    @Test
    void testLongConstructor() {
        long now = System.currentTimeMillis() / 1000;
        JTimeTransform jtt = new JTimeTransform(now);
        assertEquals(now, jtt.getTimestamp(), 1); // Allow for differences in rounding
    }

    @Test
    void testYMDConstructor() {
        JTimeTransform jtt = new JTimeTransform(2023, 2, 25); // Mar 25, 2023 (month is 0-based)
        assertEquals(2023, jtt.getYear());
        assertEquals(3, jtt.getMonth());
        assertEquals(25, jtt.getDay());
    }

    @Test
    void testToStringFormat() {
        JTimeTransform jtt = new JTimeTransform(2022, 0, 2); // Jan 2, 2022
        String str = jtt.toString("yyyy-MM-dd");
        assertTrue(str.startsWith("2022-01-02"));
    }

    @Test
    void testParseSuccess() {
        JTimeTransform jtt = new JTimeTransform(2022, 11, 20); // Dec 20, 2022
        JTimeTransform result = jtt.parse("yyyy-MM-dd", "2022-12-25");
        assertNotNull(result);
        assertEquals(2022, result.getYear());
        assertEquals(12, result.getMonth());
        assertEquals(25, result.getDay());
    }

    @Test
    void testParseFailure() {
        JTimeTransform jtt = new JTimeTransform(2022, 11, 20);
        JTimeTransform result = jtt.parse("yyyy-MM-dd", "abc");
        assertNull(result);
    }

    @Test
    void testRecentDateFormat() {
        // Use a fixed point in time to simulate
        long now = System.currentTimeMillis() / 1000;
        JTimeTransform justNow = new JTimeTransform(now);
        JTimeTransform oneMinAgo = new JTimeTransform(now - 60);
        JTimeTransform oneHourAgo = new JTimeTransform(now - 3600);
        JTimeTransform yesterday = new JTimeTransform(now - 86400);
        JTimeTransform tomorrow = new JTimeTransform(now + 86400);

        JTimeTransform.RecentDateFormat rdf = new JTimeTransform.RecentDateFormat("yyyy-MM-dd");

        // Test '前'
        String secText = rdf.format(new JTimeTransform(now-1), 1); // delta=1
        assertTrue(secText.contains("秒前") || secText.contains("秒")); // localization

        String minText = rdf.format(oneMinAgo, 60*1);
        assertTrue(minText.contains("分钟前"));

        String hourText = rdf.format(oneHourAgo, 3600);
        assertTrue(hourText.contains("小时前"));

        // Test toString(DateFormat) also
        String dtText = oneMinAgo.toString(rdf);
        assertNotNull(dtText);

        // Future times ('后')
        String futureSec = rdf.format(new JTimeTransform(now+1), -1);
        assertTrue(futureSec.contains("秒后") || futureSec.contains("秒"));

        String futureMin = rdf.format(new JTimeTransform(now+80), -80);
        assertTrue(futureMin.contains("分钟后"));

        // large deltas
        String fallbackPast = rdf.format(yesterday, 86400);
        assertNotNull(fallbackPast);

        String fallbackFuture = rdf.format(tomorrow, -86400);
        assertNotNull(fallbackFuture);
    }
}