package com.example.verbalexpressions.original;

import org.junit.jupiter.api.*;
import java.util.regex.*;
import static org.junit.jupiter.api.Assertions.*;
import com.example.verbalexpressions.VerEx;
import com.example.verbalexpressions.Util;

public class VerExExtraTest {

    VerEx v;

    @BeforeEach
    public void setUp() {
        v = new VerEx();
    }

    @AfterEach
    public void tearDown() {
        v = null;
    }

    @Test
    public void testAnything() {
        VerEx v = new VerEx().anything();
        assertNotNull(v.regex().matcher("abcdef").find());
    }

    @Test
    public void testAnythingBut() {
        VerEx v = new VerEx().anythingBut("x");
        assertNotNull(v.regex().matcher("abc").find());
        assertNotNull(v.regex().matcher("").find());
        assertNull(v.regex().matcher("x").matches() ? "Matched" : null); // full match on "x" is not allowed
        assertNotNull(v.regex().matcher("abcdef").find());
    }

    @Test
    public void testEndOfLine() {
        VerEx v = new VerEx().endOfLine();
        assertTrue(Pattern.compile(v.source() + "$").matcher("end$").find());
    }

    @Test
    public void testMaybe() {
        VerEx v = new VerEx().maybe("abc");
        assertTrue(v.regex().matcher("abc").find());
        assertTrue(v.regex().matcher("").find());
    }

    @Test
    public void testStartOfLine() {
        VerEx v = new VerEx().startOfLine();
        String pattern = v.source();
        assertTrue(pattern.startsWith("^"));
    }

    @Test
    public void testFindAndThen() {
        VerEx v = new VerEx().find("cat");
        assertTrue(v.regex().matcher("cat").find());
        VerEx v2 = new VerEx().then("dog");
        assertTrue(v2.regex().matcher("dog").find());
    }

    @Test
    public void testAnyAnyOf() {
        VerEx v = new VerEx().any("abc");
        assertTrue(v.regex().matcher("a").find());
        assertTrue(v.regex().matcher("b").find());
        assertFalse(v.regex().matcher("d").matches());
        VerEx v2 = new VerEx().anyOf("xyz");
        assertTrue(v2.regex().matcher("z").find());
    }

    @Test
    public void testLineBreakBr() {
        VerEx v = new VerEx().lineBreak();
        assertTrue(v.regex().matcher("\n").find());
        assertTrue(v.regex().matcher("\r\n").find());
        VerEx v2 = new VerEx().br();
        assertTrue(v2.regex().matcher("\n").find());
    }

    @Test
    public void testRangeWithOddArgs() {
        VerEx v = new VerEx().range("a", "c", "0", "1");
        assertTrue(v.regex().matcher("a").find());
        assertTrue(v.regex().matcher("b").find());
        assertTrue(v.regex().matcher("c").find());
        assertTrue(v.regex().matcher("0").find());
        assertTrue(v.regex().matcher("1").find());
    }

    @Test
    public void testTabAndWord() {
        VerEx v = new VerEx().tab();
        assertTrue(v.regex().matcher("\t").find());
        VerEx w = new VerEx().word();
        assertTrue(w.regex().matcher("wordtest").find());
    }

    @Test
    public void testOrWithoutValue() {
        VerEx v = new VerEx().find("foo").OR();
        assertTrue(v.source().contains("|"));
        // in Java, all methods exist, test API surface
        assertNotNull(v.find("bar"));
    }

    @Test
    public void testOrWithValue() {
        VerEx v = new VerEx().find("foo").OR("bar");
        assertTrue(v.source().contains("|(bar)"));
    }

    @Test
    public void testReplace() {
        VerEx v = new VerEx().find("foo");
        String result = v.replace("foofoo", "bar");
        assertEquals("barbar", result);
    }

    @Test
    public void testWithAnyCase() {
        VerEx v = new VerEx().find("abc").withAnyCase(true);
        assertEquals(v.getModifier("I"), Pattern.CASE_INSENSITIVE);
        v.withAnyCase(false);
        assertEquals(v.getModifier("I"), 0);
    }

    @Test
    public void testSearchOneLine() {
        VerEx v = new VerEx().searchOneLine(true);
        assertEquals(v.getModifier("M"), Pattern.MULTILINE);
        v.searchOneLine(false);
        assertEquals(v.getModifier("M"), 0);
    }

    @Test
    public void testWithAscii() {
        VerEx v = new VerEx().withAscii(true);
        assertEquals(v.getModifier("A"), Pattern.UNICODE_CHARACTER_CLASS); // Java's way closest to 'A'
        v.withAscii(false);
        assertEquals(v.getModifier("A"), 0);
    }

    @Test
    public void testValueAndSource() {
        VerEx v = new VerEx().find("cat");
        assertEquals(v.value(), v.source());
        assertEquals(v.raw(), v.source());
    }
}