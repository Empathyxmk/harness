package io.paperdb;

import org.junit.Test;
import static org.junit.Assert.*;

public class PaperTableTest {

    @Test
    public void testDefaultConstructor() {
        PaperTable<String> pt = new PaperTable<>();
        assertNull(pt.mContent);
    }

    @Test
    public void testConstructorWithContent() {
        PaperTable<Integer> pt = new PaperTable<>(100);
        assertEquals(Integer.valueOf(100), pt.mContent);
    }
}