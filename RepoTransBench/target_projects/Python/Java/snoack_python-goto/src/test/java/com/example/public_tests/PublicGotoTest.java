package com.example.public_tests;

import com.example.goto.Goto;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;

import static org.junit.jupiter.api.Assertions.*;

class PublicGotoTest {

    @Test
    void test_goto_has_no_goto_and_label_by_default() {
        // Check that the 'Goto' class does not expose 'goto' or 'label' attributes by default
        Field[] fields = Goto.class.getDeclaredFields();
        boolean hasGoto = false, hasLabel = false;
        for (Field f : fields) {
            if (f.getName().equals("goto")) hasGoto = true;
            if (f.getName().equals("label")) hasLabel = true;
        }
        assertFalse(hasGoto, "Goto class should not have a 'goto' field");
        assertFalse(hasLabel, "Goto class should not have a 'label' field");
    }

    @Test
    void test_goto_module_has_file_attribute() {
        try {
            Field f = Goto.class.getDeclaredField("__file__");
            assertNotNull(f);
            assertTrue(f.getType().equals(String.class));
        } catch (NoSuchFieldException e) {
            fail("Goto class should have a __file__ attribute");
        }
    }

    @Test
    void test_goto_module_name_is_goto() {
        try {
            Field f = Goto.class.getDeclaredField("__name__");
            assertEquals("goto", (String) f.get(null));
        } catch (Exception e) {
            fail("Goto class should have a __name__ attribute");
        }
    }
}