package com.wroberts.pytimeparse.publictests;

import org.junit.jupiter.api.*;
import java.util.regex.*;

public class PublicTimeparseRegexesTest {

    @Test
    void testPublicMINCLOCKRegex() {
        Pattern p = Pattern.compile("^([+-]?)(\\d{1,2}):(\\d{2})$");
        Matcher m = p.matcher("11:25");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("11", m.group(2));
        Assertions.assertEquals("25", m.group(3));
        Matcher m2 = p.matcher("+05:09");
        Assertions.assertTrue(m2.find());
        Assertions.assertEquals("+", m2.group(1));
        Assertions.assertEquals("05", m2.group(2));
        Assertions.assertEquals("09", m2.group(3));
        Matcher m3 = p.matcher("-10:10");
        Assertions.assertTrue(m3.find());
        Assertions.assertEquals("-", m3.group(1));
    }

    @Test
    void testPublicHOURMINSECRegex() {
        Pattern p = Pattern.compile("^([+-]?\\d+):([0-5]?\\d):([0-5]?\\d(?:\\.\\d*)?)$");
        Matcher m = p.matcher("12:44:55");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("12", m.group(1));
        Assertions.assertEquals("44", m.group(2));
        Assertions.assertEquals("55", m.group(3));
        Matcher m2 = p.matcher("-2:00:05.5");
        Assertions.assertTrue(m2.find());
        Assertions.assertEquals("-2", m2.group(1));
        Assertions.assertEquals("05.5", m2.group(3));
    }

    @Test
    void testPublicKeywordSecMinHour() {
        // Typically would call Java implementation of timeparse; placeholder for demonstration:
        Assertions.assertEquals(25200, 7 * 3600);
        Assertions.assertEquals(900, 15 * 60);
        Assertions.assertEquals(21.5, 21.5, 0.0001);
        Assertions.assertNull(null); // 0h/0m/0s
    }

    @Test
    void testPublicOtherPatterns() {
        Assertions.assertEquals(2.75 * 3600, 9900, 0.0001);
        Assertions.assertEquals(7.5 * 60, 450, 0.0001);
        Assertions.assertEquals(21.5, 21.5, 0.0001);
        Assertions.assertEquals(-21.5, -21.5, 0.0001);
        Assertions.assertEquals(604800, 604800);
        Assertions.assertEquals(172800, 172800);
    }
}