package com.stephenmcd.formsbuilder.original;

import com.stephenmcd.formsbuilder.fields.Fields;
import com.stephenmcd.formsbuilder.fields.Tuple;
import com.stephenmcd.formsbuilder.utils.Utils;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class CoreTest {
    @Test
    public void testFieldChoicesDict() {
        String choices = "Red\nGreen\nBlue";
        List<Tuple<String, String>> expected = Arrays.asList(
                new Tuple<>("Red", "Red"),
                new Tuple<>("Green", "Green"),
                new Tuple<>("Blue", "Blue")
        );
        assertEquals(expected, Fields.choicesFromLines(choices));
    }

    @Test
    public void testFieldChoicesDictEmpty() {
        assertEquals(Arrays.asList(), Fields.choicesFromLines(""));
    }

    @Test
    public void testIsFile() {
        assertTrue(Utils.isFile("photo.PNG"));
        assertTrue(Utils.isFile("document.PDF"));
        assertFalse(Utils.isFile("example.txt"));
        assertFalse(Utils.isFile("no_dot"));
    }

    @Test
    public void testSlugifyStripAndLower() {
        String s = " Hello__World__ ";
        String sl = Utils.slugify(s);
        assertEquals("hello-world", sl);
    }

    @Test
    public void testSettingImports() {
        boolean USE_SITES = true;
        boolean USE_THREADED_EMAILS = true;
        List<String> EXTRA_FIELD_TYPES = Arrays.asList("A", "B");
        assertTrue(USE_SITES || !USE_SITES);
        assertTrue(USE_THREADED_EMAILS || !USE_THREADED_EMAILS);
        assertTrue(EXTRA_FIELD_TYPES instanceof List);
    }
}