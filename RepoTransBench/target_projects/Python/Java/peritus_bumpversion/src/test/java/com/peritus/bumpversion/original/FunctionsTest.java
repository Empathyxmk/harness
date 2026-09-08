package com.peritus.bumpversion.original;

import com.peritus.bumpversion.functions.NumericFunction;
import com.peritus.bumpversion.functions.ValuesFunction;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FunctionsTest {

    // NumericFunction

    @Test
    void testNumericInitWoFirstValue() {
        NumericFunction func = new NumericFunction();
        assertEquals("0", func.getFirstValue());
    }

    @Test
    void testNumericInitWFirstValue() {
        NumericFunction func = new NumericFunction("5");
        assertEquals("5", func.getFirstValue());
    }

    @Test
    void testNumericInitNonNumericFirstValue() {
        assertThrows(IllegalArgumentException.class, () -> {
            new NumericFunction("a");
        });
    }

    @Test
    void testNumericBumpSimpleNumber() {
        NumericFunction func = new NumericFunction();
        assertEquals("1", func.bump("0"));
    }

    @Test
    void testNumericBumpPrefixAndSuffix() {
        NumericFunction func = new NumericFunction();
        assertEquals("v1b", func.bump("v0b"));
    }

    // ValuesFunction

    @Test
    void testValuesInit() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 1, 2});
        assertEquals(0, func.getOptionalValue());
        assertEquals(0, func.getFirstValue());
    }

    @Test
    void testValuesInitWCorrectOptionalValue() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 1, 2}, 1, null);
        assertEquals(1, func.getOptionalValue());
        assertEquals(0, func.getFirstValue());
    }

    @Test
    void testValuesInitWCorrectFirstValue() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 1, 2}, null, 1);
        assertEquals(0, func.getOptionalValue());
        assertEquals(1, func.getFirstValue());
    }

    @Test
    void testValuesInitWCorrectOptionalAndFirstValue() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 1, 2}, 0, 1);
        assertEquals(0, func.getOptionalValue());
        assertEquals(1, func.getFirstValue());
    }

    @Test
    void testValuesInitWEmptyValues() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new Object[]{}));
    }

    @Test
    void testValuesInitWIncorrectOptionalValue() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new Object[]{0, 1, 2}, 3, null));
    }

    @Test
    void testValuesInitWIncorrectFirstValue() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new Object[]{0, 1, 2}, null, 3));
    }

    @Test
    void testValuesBump() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 5, 10});
        assertEquals(5, func.bump(0));
    }

    @Test
    void testValuesBump_Exception() {
        ValuesFunction func = new ValuesFunction(new Object[]{0, 5, 10});
        assertThrows(IllegalArgumentException.class, () -> func.bump(10));
    }
}