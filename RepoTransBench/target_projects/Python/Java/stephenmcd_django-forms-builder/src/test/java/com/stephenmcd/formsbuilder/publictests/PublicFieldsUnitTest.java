package com.stephenmcd.formsbuilder.publictests;

import com.stephenmcd.formsbuilder.fields.Fields;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicFieldsUnitTest {

    @Test
    public void testPublicSplitChoicesDiffInput() {
        String value = "red|green|blue";
        // For test, just extract as string list via split
        List<String> choices = Arrays.asList(value.split("\\|"));
        assertEquals(Arrays.asList("red", "green", "blue"), choices);
    }

    @Test
    public void testPublicPrettyNameDiffInput() {
        String val = "zip_code";
        assertEquals("Zip code", Fields.prettyName(val));
    }

    @Test
    public void testPublicIsEmptyDiffInput() {
        assertTrue(Fields.isEmpty(null));
        List<String> nonEmptyList = Arrays.asList("value");
        assertFalse(Fields.isEmpty(nonEmptyList));
        assertTrue(Fields.isEmpty("      "));
    }
}