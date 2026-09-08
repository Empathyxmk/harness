package com.example.verbalexpressions.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.example.verbalexpressions.VerEx;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PublicVerExTest {

    private boolean isFullMatch(VerEx v, String s) {
        Matcher m = v.match(s);
        return m != null && m.group(0).equals(s);
    }

    @Test
    public void testPublicStartOfLine() {
        VerEx verex = new VerEx().startOfLine().then("Begin");
        String s = "BeginAgain";
        String notS = "NotBegin";
        assertNotNull(verex.match(s));
        assertNull(verex.match(notS));
    }

    @Test
    public void testPublicAnything() {
        VerEx verex = new VerEx().anything();
        assertNotNull(verex.match("Some string"));
        assertNotNull(verex.match(""));
    }

    @Test
    public void testPublicAnythingBut() {
        VerEx verex = new VerEx().anythingBut("xyz");
        assertNotNull(verex.match("Hello world"));
        Matcher m = verex.match("xyzworld");
        assertNotNull(m);
        assertEquals("", m.group(0));
    }

    @Test
    public void testPublicEndOfLine() {
        VerEx verex = new VerEx().find("complete").endOfLine();
        assertTrue(verex.search("mission complete"));
        assertNull(verex.match("completely done"));
    }

    @Test
    public void testPublicMaybe() {
        VerEx verex = new VerEx().then("red").maybe("car");
        assertTrue(isFullMatch(verex, "red"));
        assertTrue(isFullMatch(verex, "redcar"));
        assertFalse(isFullMatch(verex, "redcars"));
    }

    @Test
    public void testPublicAnyOf() {
        VerEx verex = new VerEx().any("wxyz");
        assertNotNull(verex.match("z"));
        assertNotNull(verex.match("yell"));
        assertNull(verex.match("k"));
    }

    @Test
    public void testPublicNotOf() {
        VerEx verex = new VerEx().anythingBut("LMN");
        assertNotNull(verex.match("abcde"));
        Matcher m = verex.match("MMM");
        assertNotNull(m);
        assertEquals("", m.group(0));
    }

    @Test
    public void testPublicReplace() {
        VerEx verex = new VerEx().find("swap_me");
        String text = "swap_me";
        String result = verex.replace("changed", text);
        assertEquals("changed", result);
    }
}