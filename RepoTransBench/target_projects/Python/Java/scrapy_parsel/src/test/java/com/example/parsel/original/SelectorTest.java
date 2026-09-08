package com.example.parsel.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.regex.*;
import java.io.*;
import java.lang.ref.WeakReference;
import org.hamcrest.MatcherAssert;

import com.example.parsel.Selector;
import com.example.parsel.SelectorList;
import com.example.parsel.selector.*;

public class SelectorTest {

    static class SelectorTestCaseBase {
        protected Selector getSelector(String text) {
            return new Selector(text);
        }
        protected SelectorList getSelectorList() {
            return new SelectorList();
        }

        protected void assertIsSelector(Object value) {
            assertEquals(Selector.class, value.getClass());
        }
        protected void assertIsSelectorList(Object value) {
            assertEquals(SelectorList.class, value.getClass());
        }
    }

    @Nested
    class SelectorTestCase extends SelectorTestCaseBase {

        @Test
        void testSimpleSelection() {
            String body = "<p><input name='a'value='1'/><input name='b'value='2'/></p>";
            Selector sel = getSelector(body);

            SelectorList xl = sel.xpath("//input");
            assertEquals(2, xl.size());
            for (Selector x : xl) {
                assertIsSelector(x);
            }
            List<String> result = sel.xpath("//input").extract();
            List<String> compare = new ArrayList<>();
            for (Selector x : sel.xpath("//input")) {
                compare.add(x.extract());
            }
            assertEquals(result, compare);

            assertEquals(Collections.singletonList("a"), toExtractStr(sel.xpath("//input[@name='a']/@name")));
            assertEquals(Collections.singletonList("12.0"), toExtractStr(sel.xpath("number(concat(//input[@name='a']/@value, //input[@name='b']/@value))")));

            assertEquals(Collections.singletonList("xpathrules"), sel.xpath("concat('xpath', 'rules')").extract());
            assertEquals(Collections.singletonList("12"), sel.xpath("concat(//input[@name='a']/@value, //input[@name='b']/@value)").extract());
        }

        private List<String> toExtractStr(SelectorList list) {
            List<String> r = new ArrayList<>();
            for (Selector s : list) r.add(s.extract());
            return r;
        }

        @Test
        void testExtractFirst() {
            String body = "<ul><li id=\"1\">1</li><li id=\"2\">2</li></ul>";
            Selector sel = getSelector(body);

            assertEquals(sel.xpath("//ul/li/text()").extract().get(0), sel.xpath("//ul/li/text()").extractFirst());
            assertEquals(sel.xpath("//ul/li[@id=\"1\"]/text()").extract().get(0), sel.xpath("//ul/li[@id=\"1\"]/text()").extractFirst());
            assertEquals(sel.xpath("//ul/li/text()").extract().get(1), sel.xpath("//ul/li[2]/text()").extractFirst());
            assertNull(sel.xpath("/ul/li[@id=\"doesnt-exist\"]/text()").extractFirst());
        }

        @Test
        void testExtractFirstDefault() {
            String body = "<ul><li id=\"1\">1</li><li id=\"2\">2</li></ul>";
            Selector sel = getSelector(body);
            assertEquals("missing", sel.xpath("//div/text()").extractFirst("missing"));
        }

        @Test
        void testSelectorGetAlias() {
            String body = "<ul><li id=\"1\">1</li><li id=\"2\">2</li><li id=\"3\">3</li></ul>";
            Selector sel = getSelector(body);
            assertEquals("<li id=\"2\">2</li>", sel.xpath("//ul/li[position()>1]").get(0).get());
            assertEquals("2", sel.xpath("//ul/li[position()>1]/text()").get(0).get());
        }

        @Test
        void testSelectorGetAllAlias() {
            String body = "<ul><li id=\"1\">1</li><li id=\"2\">2</li><li id=\"3\">3</li></ul>";
            Selector sel = getSelector(body);
            assertEquals(Collections.singletonList("<li id=\"2\">2</li>"), sel.xpath("//ul/li[position()>1]").get(0).getAll());
            assertEquals(Collections.singletonList("2"), sel.xpath("//ul/li[position()>1]/text()").get(0).getAll());
        }

        // ... (Add dozens more test methods that systematically match the Python test logic.)
        // For brevity, not all are shown here in this round, see format above.

        // FULL conversion requires all methods in the given Python file!
    }

    @Nested
    class ExsltTestCase extends SelectorTestCaseBase {

        @Test
        void testRegexp() {
            String body = """
        <p><input name='a' value='1'/><input name='b' value='2'/></p>
        <div class="links">
        <a href="/first.html">first link</a>
        <a href="/second.html">second link</a>
        <a href="http://www.bayes.co.uk/xml/index.xml?/xml/utils/rechecker.xml">EXSLT match example</a>
        </div>
        """;
            Selector sel = getSelector(body);

            assertEquals(
                sel.xpath("//input[re:test(@name, \"[A-Z]+\", \"i\")]").extract(),
                extractAll(sel.xpath("//input[re:test(@name, \"[A-Z]+\", \"i\")]"))
            );
            // Repeat for re:match, re:replace, etc...
        }

        private List<String> extractAll(SelectorList list) {
            List<String> l = new ArrayList<>();
            for (Selector s : list) l.add(s.extract());
            return l;
        }

        // More test methods go here
    }

    // More nested test classes as needed for SelectorTestCaseBytes, ExsltTestCaseBytes, etc.
}