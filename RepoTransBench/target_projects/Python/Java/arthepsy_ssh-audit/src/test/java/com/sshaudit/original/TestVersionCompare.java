package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestVersionCompare {

    // A simple version compare utility, matching typical "1.2 < 1.4.8 > 1.4.8b > 1.5"
    public static int versionCompare(String v1, String v2) {
        if (v1 == null && v2 == null)
            return 0;
        if (v1 == null)
            return -1;
        if (v2 == null)
            return 1;
        String[] a = v1.split("\\.");
        String[] b = v2.split("\\.");
        int len = Math.max(a.length, b.length);
        for (int i = 0; i < len; ++i) {
            String x = (i < a.length ? a[i] : "0");
            String y = (i < b.length ? b[i] : "0");
            int res = x.compareToIgnoreCase(y);
            if (isNumeric(x) && isNumeric(y)) {
                res = Integer.compare(Integer.parseInt(x), Integer.parseInt(y));
            }
            if (res != 0)
                return res;
        }
        return 0;
    }

    private static boolean isNumeric(String s) {
        return s.matches("\\d+");
    }

    @Test
    public void test_version_compare_basic() {
        assertTrue(versionCompare("1.2", "1.4.8") < 0);
        assertTrue(versionCompare("1.4.8", "1.4.8b") < 0);
        assertTrue(versionCompare("1.5.7", "1.4.8") > 0);
    }

    @Test
    public void test_version_compare_equal() {
        assertEquals(0, versionCompare("1.2.3", "1.2.3"));
        assertEquals(0, versionCompare(null, null));
    }

    @Test
    public void test_version_compare_nulls() {
        assertTrue(versionCompare(null, "1.2.3") < 0);
        assertTrue(versionCompare("2.2.3", null) > 0);
    }

    @Test
    public void test_version_compare_numeric_alpha() {
        assertTrue(versionCompare("1.4.8b", "1.5") < 0);
        assertTrue(versionCompare("1.5", "1.5b") < 0);
    }

    @Test
    public void test_version_compare_leading_zero() {
        assertEquals(0, versionCompare("1.02.03", "1.2.3"));
    }
}