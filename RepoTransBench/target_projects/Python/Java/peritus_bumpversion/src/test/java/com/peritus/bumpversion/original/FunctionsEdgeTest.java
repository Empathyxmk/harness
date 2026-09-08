package com.peritus.bumpversion.original;

import com.peritus.bumpversion.functions.NumericFunction;
import com.peritus.bumpversion.functions.ValuesFunction;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FunctionsEdgeTest {

    @Test
    void testNumericFunctionBasicBump() {
        NumericFunction nf = new NumericFunction("3");
        assertEquals("4", nf.bump("3"));
        assertEquals("100", nf.bump("99"));
    }

    @Test
    void testNumericFunctionFirstValueAndOptionalValue() {
        NumericFunction nf = new NumericFunction("00");
        assertEquals("00", nf.getFirstValue());
        assertEquals("00", nf.getOptionalValue());
    }

    @Test
    void testNumericFunctionAlphanumeric() {
        NumericFunction nf = new NumericFunction("r3");
        assertEquals("r4", nf.bump("r3"));
        NumericFunction nf2 = new NumericFunction("r3-001");
        assertEquals("r4-001", nf2.bump("r3-001"));
    }

    @Test
    void testNumericFunctionInvalidFirstValue() {
        assertThrows(IllegalArgumentException.class, () -> new NumericFunction("abc"));
    }

    @Test
    void testNumericFunctionNoDigits() {
        NumericFunction n = new NumericFunction();
        assertThrows(IllegalArgumentException.class, () -> n.bump("abc"));
    }

    @Test
    void testValuesFunctionBumpAndErrors() {
        ValuesFunction vf = new ValuesFunction(new String[]{"alpha", "beta", "rc", "final"});
        assertEquals("beta", vf.bump("alpha"));
        assertEquals("rc", vf.bump("beta"));
        assertEquals("final", vf.bump("rc"));
        assertThrows(IllegalArgumentException.class, () -> vf.bump("final"));
    }

    @Test
    void testValuesFunctionInvalidEmpty() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new String[]{}));
    }

    @Test
    void testValuesFunctionOptionalValueNotInValues() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new String[]{"a", "b"}, "c", null));
    }

    @Test
    void testValuesFunctionFirstValueNotInValues() {
        assertThrows(IllegalArgumentException.class, () -> new ValuesFunction(new String[]{"a", "b"}, null, "c"));
    }

}