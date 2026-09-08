package org.nibblesec.tools;

import org.junit.Test;

import java.util.ArrayList;
import java.util.regex.Pattern;

import static org.junit.Assert.*;

public class PatternListPublicTest {
    @Test
    public void testPatternMatchingWithNewPattern() {
        ArrayList<Pattern> patterns = new ArrayList<>();
        patterns.add(Pattern.compile("^PUBLIC_\\d+$"));
        patterns.add(Pattern.compile("TestCase.*"));

        String value1 = "PUBLIC_1234";
        String value2 = "TestCasePublic";
        String value3 = "NotMatching";

        assertTrue(patterns.get(0).matcher(value1).matches());
        assertFalse(patterns.get(0).matcher(value2).matches());

        assertTrue(patterns.get(1).matcher(value2).matches());
        assertFalse(patterns.get(1).matcher(value3).matches());
    }
}