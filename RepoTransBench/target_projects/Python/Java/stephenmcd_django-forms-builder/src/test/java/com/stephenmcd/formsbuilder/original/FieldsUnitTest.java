package com.stephenmcd.formsbuilder.original;

import com.stephenmcd.formsbuilder.fields.Fields;
import com.stephenmcd.formsbuilder.fields.Tuple;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class FieldsUnitTest {

    @Test
    public void testSplitChoicesString() {
        String s = "Red\nBlue\r\nGreen";
        List<Tuple<String, String>> result = Fields.splitChoices(s);
        List<Tuple<String, String>> expected = Arrays.asList(
                new Tuple<>("Red", "Red"),
                new Tuple<>("Blue", "Blue"),
                new Tuple<>("Green", "Green")
        );
        assertEquals(expected, result);
    }

    @Test
    public void testSplitChoicesEmpty() {
        assertEquals(Collections.emptyList(), Fields.splitChoices(""));
        assertEquals(Collections.emptyList(), Fields.splitChoices(null));
        assertEquals(Collections.emptyList(), Fields.splitChoices(0));
        assertEquals(Collections.emptyList(), Fields.splitChoices(3.14));
    }

    @Test
    public void testSplitChoicesListOfTuples() {
        List<Tuple<String, String>> lst = Arrays.asList(
                new Tuple<>("A", "Apple"),
                new Tuple<>("B", "Banana")
        );
        assertEquals(lst, Fields.splitChoices(lst));
    }

    @Test
    public void testSplitChoicesTupleOfTuples() {
        Tuple<String, String>[] tpl = new Tuple[]{
                new Tuple<>("A", "Apple"),
                new Tuple<>("B", "Banana")
        };
        List<Tuple<String, String>> result = Fields.splitChoices(tpl);
        List<Tuple<String, String>> expected = Arrays.asList(tpl);
        assertEquals(expected, result);
    }

    @Test
    public void testSplitChoicesLeadingTrailingWhitespace() {
        String s = " Red \n\n Blue";
        List<Tuple<String, String>> result = Fields.splitChoices(s);
        List<Tuple<String, String>> expected = Arrays.asList(
                new Tuple<>("Red", "Red"),
                new Tuple<>("Blue", "Blue")
        );
        assertEquals(expected, result);
    }

    @Test
    public void testAliasChoicesFromLines() {
        String s = "One\nTwo";
        List<Tuple<String, String>> result = Fields.choicesFromLines(s);
        List<Tuple<String, String>> expected = Arrays.asList(
                new Tuple<>("One", "One"),
                new Tuple<>("Two", "Two")
        );
        assertEquals(expected, result);
    }

    @Test
    public void testFieldChoicesAndTypes() {
        assertTrue(Fields.FIELD_CHOICES instanceof List);
        assertTrue(Fields.FIELD_TYPES instanceof List);
        assertTrue(Fields.FIELD_TYPES.stream().allMatch(i -> i instanceof Tuple));
        List<Tuple<String, String>> expected = new ArrayList<>();
        for (Tuple<String, String> kv : Fields.FIELD_CHOICES) {
            expected.add(new Tuple<>(kv.fst, kv.snd));
        }
        assertEquals(expected, Fields.FIELD_TYPES);
    }
}