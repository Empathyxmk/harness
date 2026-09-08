package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Arrays;

class StreamerTest {
    static class Streamer {
        List<String> lines;
        int idx = 0;
        Streamer(List<String> lines) { this.lines = lines; }
        String next() {
            if (idx < lines.size()) return lines.get(idx++);
            throw new IndexOutOfBoundsException();
        }
        boolean hasNext() { return idx < lines.size(); }
    }

    @Test
    void testStreamerIteratesLines() {
        Streamer s = new Streamer(Arrays.asList("1", "2", "3"));
        assertTrue(s.hasNext());
        assertEquals("1", s.next());
        assertTrue(s.hasNext());
        assertEquals("2", s.next());
        assertTrue(s.hasNext());
        assertEquals("3", s.next());
        assertFalse(s.hasNext());
    }

    @Test
    void testStreamerThrowsWhenExhausted() {
        Streamer s = new Streamer(Arrays.asList("one"));
        assertEquals("one", s.next());
        assertThrows(IndexOutOfBoundsException.class, s::next);
    }
}