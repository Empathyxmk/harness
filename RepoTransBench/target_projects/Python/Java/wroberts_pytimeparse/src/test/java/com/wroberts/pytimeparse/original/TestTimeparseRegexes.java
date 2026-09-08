package com.wroberts.pytimeparse.original;

import org.junit.jupiter.api.*;
import java.util.regex.*;

public class TestTimeparseRegexes {

    public static final String WEEKS = "^(?<weeks>(?:[0-9]+\\.?[0-9]*))\\s*(w|wk|wks|weeks?)$";
    public static final String DAYS = "^(?<days>(?:[0-9]+\\.?[0-9]*))\\s*(d|dy|dys|days?)$";
    public static final String HOURS = "^(?<hours>(?:[0-9]+\\.?[0-9]*))\\s*(h|hr|hrs|hour|hours?)$";
    public static final String MINS = "^(?<mins>(?:[0-9]+\\.?[0-9]*))\\s*(m|min|mins|minute|minutes?)$";
    public static final String SECS = "^(?<secs>(?:[0-9]+\\.?[0-9]*))\\s*(s|sec|secs|second|seconds?)$";
    public static final String MINCLOCK = "^(?<mins>[0-9]{1,2}):(?<secs>[0-9]+\\.?[0-9]*)$";
    public static final String HOURCLOCK = "^(?<hours>[0-9]+):(?<mins>[0-5]?[0-9]):(?<secs>[0-5]?[0-9](?:\\.[0-9]*)?)$";
    public static final String DAYCLOCK = "^(?<days>[0-9]+):(?<hours>[0-2]?[0-9]):(?<mins>[0-5]?[0-9]):(?<secs>[0-5]?[0-9](?:\\.[0-9]*)?)$";

    @Test
    void testWeeksRegex() {
        String[] vals = {"2w", "2wk", "2wks", "2weeks"};
        Pattern pat = Pattern.compile(WEEKS, Pattern.CASE_INSENSITIVE);
        for (String val : vals) {
            Matcher m = pat.matcher(val);
            Assertions.assertTrue(m.find());
            Assertions.assertEquals("2", m.group("weeks"));
        }
    }

    @Test
    void testDaysRegex() {
        String[] vals = {"4d", "4dy", "4dys", "4days"};
        Pattern pat = Pattern.compile(DAYS, Pattern.CASE_INSENSITIVE);
        for (String val : vals) {
            Matcher m = pat.matcher(val);
            Assertions.assertTrue(m.find());
            Assertions.assertEquals("4", m.group("days"));
        }
        Matcher m = pat.matcher("1.5days");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("1.5", m.group("days"));
    }

    @Test
    void testHoursRegex() {
        String[] vals = {"7h", "7hr", "7hrs", "7hour", "7hours"};
        Pattern pat = Pattern.compile(HOURS, Pattern.CASE_INSENSITIVE);
        for (String val : vals) {
            Matcher m = pat.matcher(val);
            Assertions.assertTrue(m.find());
            Assertions.assertEquals("7", m.group("hours"));
        }
        Matcher m = pat.matcher("2.5hrs");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("2.5", m.group("hours"));
    }

    @Test
    void testMinsRegex() {
        String[] vals = {"9m", "9min", "9mins", "9minute", "9minutes"};
        Pattern pat = Pattern.compile(MINS, Pattern.CASE_INSENSITIVE);
        for (String val : vals) {
            Matcher m = pat.matcher(val);
            Assertions.assertTrue(m.find());
            Assertions.assertEquals("9", m.group("mins"));
        }
        Matcher m = pat.matcher("0.5min");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("0.5", m.group("mins"));
    }

    @Test
    void testSecsRegex() {
        String[] vals = {"15s", "15sec", "15secs", "15second", "15seconds"};
        Pattern pat = Pattern.compile(SECS, Pattern.CASE_INSENSITIVE);
        for (String val : vals) {
            Matcher m = pat.matcher(val);
            Assertions.assertTrue(m.find());
            Assertions.assertEquals("15", m.group("secs"));
        }
        Matcher m = pat.matcher("3.25s");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("3.25", m.group("secs"));
    }

    @Test
    void testMinclockRegex() {
        Pattern pat = Pattern.compile(MINCLOCK, Pattern.CASE_INSENSITIVE);
        Matcher m = pat.matcher("3:09");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("3", m.group("mins"));
        Assertions.assertEquals("09", m.group("secs"));
        m = pat.matcher("5:30.5");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("5", m.group("mins"));
        Assertions.assertEquals("30.5", m.group("secs"));
    }

    @Test
    void testHourclockRegex() {
        Pattern pat = Pattern.compile(HOURCLOCK, Pattern.CASE_INSENSITIVE);
        Matcher m = pat.matcher("10:23:59");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("10", m.group("hours"));
        Assertions.assertEquals("23", m.group("mins"));
        Assertions.assertEquals("59", m.group("secs"));
        m = pat.matcher("1:01:01.1");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("1", m.group("hours"));
        Assertions.assertEquals("01", m.group("mins"));
        Assertions.assertEquals("01.1", m.group("secs"));
    }

    @Test
    void testDayclockRegex() {
        Pattern pat = Pattern.compile(DAYCLOCK, Pattern.CASE_INSENSITIVE);
        Matcher m = pat.matcher("2:10:23:12");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("2", m.group("days"));
        Assertions.assertEquals("10", m.group("hours"));
        Assertions.assertEquals("23", m.group("mins"));
        Assertions.assertEquals("12", m.group("secs"));
        m = pat.matcher("2:10:23:12.249");
        Assertions.assertTrue(m.find());
        Assertions.assertEquals("12.249", m.group("secs"));
    }
}