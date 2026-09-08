package com.stephenmcd.formsbuilder.publictests;

import com.stephenmcd.formsbuilder.fields.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;

public class PublicFieldsTest {

    @Test
    public void testPublicFieldToPythonBooleanTrue() {
        BooleanField booleanField = new BooleanField();
        assertTrue(booleanField.toPython("on"));
    }

    @Test
    public void testPublicFieldToPythonBooleanFalse() {
        BooleanField booleanField = new BooleanField();
        assertFalse(booleanField.toPython(""));
        assertFalse(booleanField.toPython(null));
    }

    @Test
    public void testPublicFieldToPythonSelect() {
        SelectField selectField = new SelectField("orange|banana|pear");
        assertEquals(Arrays.asList("orange", "banana", "pear"), selectField.choices);
    }

    @Test
    public void testPublicPrettyNameWithNumber() {
        assertEquals("Item 123 value", Fields.prettyName("item_123_value"));
    }
}