package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;

import java.nio.charset.StandardCharsets;

public class ContentDetectorTest {

    @Test
    public void testSimpleOrMatch() {
        String[][] clues = {{"foo"}, {"bar"}};
        ContentDetector detector = new ContentDetector(clues, 100);
        assertEquals(0, detector.getFirstMatch("foo hello world".getBytes(StandardCharsets.UTF_8)));
        assertEquals(1, detector.getFirstMatch("something bar here".getBytes(StandardCharsets.UTF_8)));
        assertEquals(-1, detector.getFirstMatch("baz qux".getBytes(StandardCharsets.UTF_8)));
    }

    @Test
    public void testAndMatch() {
        String[][] clues = {{"foo", "bar"}, {"baz"}};
        ContentDetector detector = new ContentDetector(clues, 100);
        assertEquals(0, detector.getFirstMatch("this line has foo and bar together".getBytes(StandardCharsets.UTF_8)));
        assertEquals(1, detector.getFirstMatch("some baz string".getBytes(StandardCharsets.UTF_8)));
        assertEquals(-1, detector.getFirstMatch("foo only here".getBytes(StandardCharsets.UTF_8)));
    }

    @Test
    public void testMaxOffset() {
        String[][] clues = {{"clue"}};
        ContentDetector detector = new ContentDetector(clues, 4); // should only look at first 4 bytes
        assertEquals(-1, detector.getFirstMatch("say clue later".getBytes(StandardCharsets.UTF_8)));
        assertEquals(0, detector.getFirstMatch("clue here".getBytes(StandardCharsets.UTF_8)));
    }

    @Test
    public void testMatchesConvenience() {
        String[][] clues = {{"needle"}};
        ContentDetector detector = new ContentDetector(clues, 100);
        assertTrue(detector.matches("and a needle in haystack".getBytes(StandardCharsets.UTF_8)));
        assertFalse(detector.matches("no match".getBytes(StandardCharsets.UTF_8)));
    }
}