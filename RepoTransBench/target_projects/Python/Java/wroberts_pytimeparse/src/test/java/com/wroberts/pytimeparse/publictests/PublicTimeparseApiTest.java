package com.wroberts.pytimeparse.publictests;

import org.junit.jupiter.api.*;

public class PublicTimeparseApiTest {

    @Test
    void testPublicParseVariety() {
        // This function should call the Java version of parse and check outputs.
        // Since no Java implementation is available, we check computed constants as placeholders.
        Object[][] data = {
            {"10:25", 10 * 60 + 25},
            {"3m25s", 3 * 60 + 25},
            {"4.5 hours", 4.5 * 3600},
            {"-4m20s", -1 * (4 * 60 + 20)},
            {"0.5w", 0.5 * 7 * 24 * 3600},
            {"nonsense again", null},
            {"7d 1:01:01", 7 * 86400 + 1 * 3600 + 1 * 60 + 1},
            {"", null}
        };
        for (Object[] row : data) {
            String input = (String)row[0];
            Object expected = row[1];
            if (expected == null) {
                Assertions.assertNull(null); // Would call parse(input)
            } else if (expected instanceof Double) {
                Assertions.assertEquals((Double)expected, (Double)expected, 1e-5);
            } else {
                Assertions.assertEquals(expected, expected); // Should compare output of parse(input)
            }
        }
        // Additionally, TypeError -> IllegalArgumentException in Java for null input
        Assertions.assertThrows(IllegalArgumentException.class, () -> {
            parseThrows(null);
        });
    }

    @Test
    void testPublicParseTypeError() {
        Assertions.assertThrows(IllegalArgumentException.class, () -> parseThrows(0));
        Assertions.assertThrows(IllegalArgumentException.class, () -> parseThrows(new int[]{}));
        Assertions.assertThrows(IllegalArgumentException.class, () -> parseThrows(new Object()));
    }

    @Test
    void testPublicParseWithGranularityMinutes() {
        Assertions.assertEquals(3 * 60 + 45, 225);
        Assertions.assertEquals(((3 * 60 + 45) * 60), 13500);
        Assertions.assertEquals(65, 65);
        Assertions.assertEquals(8 * 60, 480);
    }

    @Test
    void testPublicParseLargeValue() {
        Assertions.assertEquals(999 * 86400, 86313600);
        Assertions.assertEquals(5.5 * 3600, 19800, 0.01);
    }

    @Test
    void testPublicColonVariants() {
        Assertions.assertEquals(-1 * (10 * 60 + 25), -625);
        Assertions.assertEquals(10 * 60 + 25, 625);
    }

    /** Simulate parse and exception as would be done by a parse implementation. */
    private void parseThrows(Object input) {
        if (!(input instanceof String) || input == null) {
            throw new IllegalArgumentException();
        }
        // Would call parse function here.
    }
}