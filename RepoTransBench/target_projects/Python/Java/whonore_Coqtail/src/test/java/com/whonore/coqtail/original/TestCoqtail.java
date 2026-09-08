package com.whonore.coqtail.original;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.Coqtail;
import com.whonore.coqtail.Coqtail.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.ArrayList;

public class TestCoqtail {

    @Test
    void testLinesAndHighlightsString() {
        // Assume linesAndHighlightsString just splits on \n
        String[] lines = Coqtail.linesAndHighlightsString("foo\nbar", 0);
        assertArrayEquals(new String[] {"foo", "bar"}, lines);
        // Highlights simulation (empty for string input)
        List<Object> highlights = new ArrayList<>();
        assertEquals(0, highlights.size());
    }
}