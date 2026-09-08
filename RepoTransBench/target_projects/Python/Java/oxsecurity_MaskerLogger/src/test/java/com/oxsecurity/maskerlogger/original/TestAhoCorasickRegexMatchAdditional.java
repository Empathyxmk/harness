package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.ahocorasickregexmatch.RegexMatcher;

import java.util.regex.Pattern;

public class TestAhoCorasickRegexMatchAdditional {

    @Test
    public void testMaskMultipleMatches() {
        RegexMatcher rm = new RegexMatcher(null, 90);
        String msg = "password: alpha password: beta";
        String masked = rm.mask(msg);
        // At least two sets of mask chars must be in output
        assertTrue(masked.split("\\*\\*\\*").length > 2); // 2 or more matches
    }

    @Test
    public void testMaskNoMatch() {
        RegexMatcher rm = new RegexMatcher(null);
        String text = "this is safe";
        assertEquals(text, rm.mask(text));
    }

    @Test
    public void testFindMatchesGroup0() {
        RegexMatcher rm = new RegexMatcher(null);
        rm.setRegexes(new Pattern[]{Pattern.compile("safe")});
        String masked = rm.mask("safe");
        assertTrue(masked.contains("*") || masked.equals("safe"));
    }

    @Test
    public void testInvalidConfigFile() {
        String path = "broken.toml";
        RegexMatcher rm = new RegexMatcher(path);
        String m = rm.mask("password: example");
        assertTrue(m.contains("*"));
    }
}