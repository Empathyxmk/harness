package com.stephenmcd.formsbuilder.original;

import com.stephenmcd.formsbuilder.fields.Fields;
import com.stephenmcd.formsbuilder.fields.Tuple;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class FieldsTest {

    @Test
    public void testLinebreakRe() {
        assertArrayEquals(new String[]{"a", "b"}, Fields.linebreakRe.split("a\nb"));
        assertArrayEquals(new String[]{"a", "b"}, Fields.linebreakRe.split("a\r\nb"));
        assertArrayEquals(new String[]{"a", "b", "c"}, Fields.linebreakRe.split("a\r\nb\nc"));
    }

    @Test
    public void testFieldTypeIterable() {
        List<Tuple<String, String>> typesList = Fields.FIELD_TYPES;
        assertTrue(typesList instanceof List);
        for (Tuple<String, String> t : typesList) {
            assertNotNull(t);
            assertTrue(t instanceof Tuple);
        }
    }

    @Test
    public void testChoicesFromLinesBasic() {
        String choices = "Red\nGreen\nBlue";
        List<Tuple<String, String>> expected = Arrays.asList(
                new Tuple<>("Red", "Red"),
                new Tuple<>("Green", "Green"),
                new Tuple<>("Blue", "Blue")
        );
        assertEquals(expected, Fields.choicesFromLines(choices));
    }

    @Test
    public void testChoicesFromLinesEmpty() {
        assertEquals(Collections.emptyList(), Fields.choicesFromLines(""));
        assertEquals(Collections.emptyList(), Fields.choicesFromLines(null));
        assertEquals(Collections.emptyList(), Fields.choicesFromLines(1));
        // Handles basic list/tuple pass-through
        List<Tuple<String, String>> out = Fields.choicesFromLines(Arrays.asList(new Tuple<>("foo", "foo")));
        assertEquals(Arrays.asList(new Tuple<>("foo", "foo")), out);
    }
}