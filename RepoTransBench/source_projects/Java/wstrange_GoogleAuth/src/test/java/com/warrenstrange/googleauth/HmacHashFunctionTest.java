package com.warrenstrange.googleauth;

import org.junit.Test;
import static org.junit.Assert.*;

public class HmacHashFunctionTest {

    @Test
    public void testValueOf() {
        assertEquals(HmacHashFunction.valueOf("HmacSHA1"), HmacHashFunction.valueOf("HmacSHA1"));
        assertEquals(HmacHashFunction.valueOf("HmacSHA256"), HmacHashFunction.valueOf("HmacSHA256"));
        assertEquals(HmacHashFunction.valueOf("HmacSHA512"), HmacHashFunction.valueOf("HmacSHA512"));
    }

    @Test
    public void testValuesArePresent() {
        String allNames = "";
        for (HmacHashFunction fn : HmacHashFunction.values()) {
            allNames += fn.name();
        }
        assertTrue(allNames.contains("HmacSHA1"));
        assertTrue(allNames.contains("HmacSHA256"));
        assertTrue(allNames.contains("HmacSHA512"));
    }
}