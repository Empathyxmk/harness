package com.example.verbalexpressions.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.example.verbalexpressions.VerEx;
import com.example.verbalexpressions.Util;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PublicVerExExtraTest {

    @Test
    public void testReEscapePublic() {
        // Java version: Util.reEscape acts as identity function in Python tests
        assertEquals("bar(foo)", Util.reEscape("bar(foo)"));
        assertEquals("hello?world.", Util.reEscape("hello?world."));
        assertEquals("[]{}", Util.reEscape("[]{}"));
        assertEquals("+*|", Util.reEscape("+*|"));
    }

    @Test
    public void testVerexComplexPatternPublic() {
        VerEx verex = new VerEx().startOfLine().then("ftp://").maybe("downloads.").anythingBut(" ").endOfLine();
        assertNotNull(verex.match("ftp://files.com"));
        assertNotNull(verex.match("ftp://downloads.files.com"));
        assertNull(verex.match("ftp:// downloads.files.com"));
    }

    @Test
    public void testVerexAnythingButPublic() {
        VerEx verex = new VerEx().startOfLine().anythingBut("xyz").endOfLine();
        assertNotNull(verex.match("abc"));
        assertNull(verex.match("x"));
        assertNull(verex.match("y"));
        assertNotNull(verex.match(""));
    }

    @Test
    public void testVerexRangePublic() {
        VerEx verex = new VerEx().range("a", "c");
        Pattern pattern = verex.regex();
        assertTrue(pattern.matcher("xyzabc").find());
        assertTrue(pattern.matcher("b").matches());
        assertFalse(pattern.matcher("g").matches());
    }

    @Test
    public void testVerexMultipleOperatorsPublic() {
        VerEx verex = new VerEx().then("baz").maybe("qux").anything().endOfLine();
        assertNotNull(verex.match("bazquxx"));
        assertNotNull(verex.match("bazplus"));
        assertNotNull(verex.match("baz"));
    }

    @Test
    public void testVerexAnyPublic() {
        VerEx verex = new VerEx().any("QRST");
        assertNotNull(verex.match("S"));
        assertNotNull(verex.match("QRST"));
        assertNull(verex.match("P"));
    }

    @Test
    public void testVerexMatchPublic() {
        VerEx verex = new VerEx().startOfLine().then("run").maybe("ner").endOfLine();
        Matcher m = verex.match("runner");
        assertNotNull(m);
        assertEquals("runner", m.group(0));
        Matcher m2 = verex.match("run");
        assertNotNull(m2);
    }

    @Test
    public void testVerexReplacePublic() {
        VerEx verex = new VerEx().find("error");
        String text = "error";
        String replaced = verex.replace("fixed", text);
        assertEquals("fixed", replaced);
    }
}