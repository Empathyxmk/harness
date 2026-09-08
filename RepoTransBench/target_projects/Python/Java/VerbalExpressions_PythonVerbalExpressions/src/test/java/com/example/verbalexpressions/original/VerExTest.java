package com.example.verbalexpressions.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import com.example.verbalexpressions.VerEx;

public class VerExTest {

    VerEx v;
    Pattern exp;

    @BeforeEach
    public void setUp() {
        v = new VerEx();
    }

    @AfterEach
    public void tearDown() {
        v = null;
        exp = null;
    }

    @Test
    public void testShouldRenderVerexAsString() {
        assertEquals("^$", v.add("^$").toString());
    }

    @Test
    public void testShouldRenderVerexListAsString() {
        assertEquals("^[0-9]$", v.add(new String[]{"^", "[0-9]", "$"}).toString());
    }

    @Test
    public void testShouldMatchCharactersInRange() {
        exp = v.startOfLine().range("a", "c").regex();
        for (String character : new String[]{"a", "b", "c"}) {
            assertTrue(exp.matcher(character).find());
        }
    }

    @Test
    public void testShouldNotMatchCharactersOutsideOfRange() {
        exp = v.startOfLine().range("a", "c").regex();
        assertFalse(exp.matcher("d").find());
    }

    @Test
    public void testShouldMatchCharactersInExtendedRange() {
        exp = v.startOfLine().range("a", "b", "X", "Z").regex();
        for (String character : new String[]{"a", "b", "X", "Y", "Z"}) {
            assertTrue(exp.matcher(character).find());
        }
    }

    @Test
    public void testShouldNotMatchCharactersOutsideOfExtendedRange() {
        exp = v.startOfLine().range("a", "b", "X", "Z").regex();
        assertFalse(exp.matcher("c").find());
        assertFalse(exp.matcher("W").find());
    }

    @Test
    public void testShouldMatchStartOfLine() {
        exp = v.startOfLine().regex();
        assertTrue(exp.matcher("text  ").find(), "Not started :(");
    }

    @Test
    public void testShouldMatchEndOfLine() {
        exp = v.startOfLine().endOfLine().regex();
        assertTrue(exp.matcher("").find(), "It's not the end!");
    }

    @Test
    public void testShouldMatchAnything() {
        exp = v.startOfLine().anything().endOfLine().regex();
        assertTrue(exp.matcher("!@#$%¨&*()__+{}").find(), "Not so anything...");
    }

    @Test
    public void testShouldMatchAnythingButSpecifiedElementWhenElementIsNotFound() {
        exp = v.startOfLine().anythingBut("X").endOfLine().regex();
        assertTrue(exp.matcher("Y Files").find(), "Found the X!");
    }

    @Test
    public void testShouldNotMatchAnythingButSpecifiedElementWhenSpecifiedElementIsFound() {
        exp = v.startOfLine().anythingBut("X").endOfLine().regex();
        assertFalse(exp.matcher("VerEX").find(), "Didn't found the X :(");
    }

    @Test
    public void testShouldFindElement() {
        exp = v.startOfLine().find("Wally").endOfLine().regex();
        assertTrue(exp.matcher("Wally").find(), "404! Wally not Found!");
    }

    @Test
    public void testShouldNotFindMissingElement() {
        exp = v.startOfLine().find("Wally").endOfLine().regex();
        assertFalse(exp.matcher("Wall-e").find(), "DAFUQ is Wall-e?");
    }

    @Test
    public void testShouldMatchWhenMaybeElementIsPresent() {
        exp = v.startOfLine().find("Python2.").maybe("7").endOfLine().regex();
        assertTrue(exp.matcher("Python2.7").find(), "Version doesn't match!");
    }

    @Test
    public void testShouldMatchWhenMaybeElementIsMissing() {
        exp = v.startOfLine().find("Python2.").maybe("7").endOfLine().regex();
        assertTrue(exp.matcher("Python2.").find(), "Version doesn't match!");
    }

    @Test
    public void testShouldMatchOnAnyWhenElementIsFound() {
        exp = v.startOfLine().any("Q").anything().endOfLine().regex();
        assertTrue(exp.matcher("Query").find(), "No match found!");
    }

    @Test
    public void testShouldNotMatchOnAnyWhenElementIsNotFound() {
        exp = v.startOfLine().any("Q").anything().endOfLine().regex();
        assertFalse(exp.matcher("W").find(), "I've found it!");
    }

    @Test
    public void testShouldMatchWhenLineBreakPresent() {
        exp = v.startOfLine().anything().lineBreak().anything().endOfLine().regex();
        assertTrue(exp.matcher("Marco \n Polo").find(), "Give me a break!!");
    }

    @Test
    public void testShouldMatchWhenLineBreakAndCarriageReturnPresent() {
        exp = v.startOfLine().anything().lineBreak().anything().endOfLine().regex();
        assertTrue(exp.matcher("Marco \r\n Polo").find(), "Give me a break!!");
    }

    @Test
    public void testShouldNotMatchWhenLineBreakIsMissing() {
        exp = v.startOfLine().anything().lineBreak().anything().endOfLine().regex();
        assertFalse(exp.matcher("Marco Polo").find(), "There's a break here!");
    }

    @Test
    public void testShouldMatchWhenTabPresent() {
        exp = v.startOfLine().anything().tab().endOfLine().regex();
        assertTrue(exp.matcher("One tab only\t").find(), "No tab here!");
    }

    @Test
    public void testShouldNotMatchWhenTabIsMissing() {
        exp = v.startOfLine().anything().tab().endOfLine().regex();
        assertFalse(exp.matcher("No tab here").find(), "There's a tab here!");
    }

    @Test
    public void testShouldMatchWhenWordPresent() {
        exp = v.startOfLine().anything().word().endOfLine().regex();
        assertTrue(exp.matcher("Oneword").find(), "Not just a word!");
    }

    @Test
    public void testNotMatchWhenTwoWordsArePresentInsteadOfOne() {
        exp = v.startOfLine().anything().tab().endOfLine().regex();
        assertFalse(exp.matcher("Two words").find(), "I've found two of them");
    }

    @Test
    public void testShouldMatchWhenOrConditionFulfilled() {
        exp = v.startOfLine().anything().find("G").OR().find("h").endOfLine().regex();
        assertTrue(exp.matcher("Github").find(), "Octocat not found");
    }

    @Test
    public void testShouldNotMatchWhenOrConditionNotFulfilled() {
        exp = v.startOfLine().anything().find("G").OR().find("h").endOfLine().regex();
        assertFalse(exp.matcher("Bitbucket").find(), "Bucket not found");
    }

    @Test
    public void testShouldMatchOnUpperCaseWhenLowerCaseIsGivenAndAnyCaseIsTrue() {
        exp = v.startOfLine().find("THOR").endOfLine().withAnyCase(true).regex();
        assertTrue(exp.matcher("thor").find(), "Upper case Thor, please!");
    }

    @Test
    public void testShouldMatchMultipleLines() {
        exp = v.startOfLine().anything().find("Pong").anything().endOfLine().searchOneLine(true).regex();
        assertTrue(exp.matcher("Ping \n Pong \n Ping").find(), "Pong didn't answer");
    }

    @Test
    public void testShouldMatchEmailAddress() {
        exp = v.startOfLine().word().then("@").word().then(".").word().endOfLine().regex();
        assertTrue(exp.matcher("mail@mail.com").find(), "Not a valid email");
    }

    @Test
    public void testShouldMatchUrl() {
        exp = v.startOfLine().then("http").maybe("s").then("://").maybe("www.").word()
                .then(".").word().maybe("/").endOfLine().regex();
        assertTrue(exp.matcher("https://www.google.com/").find(), "Not a valid email");
    }
}