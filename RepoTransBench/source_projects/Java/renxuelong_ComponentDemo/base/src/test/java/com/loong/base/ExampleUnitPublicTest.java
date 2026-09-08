package com.loong.base;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleUnitPublicTest {
    @Test
    public void stringConcat_isCorrect() {
        String a = "base";
        String b = "Public";
        assertEquals("basePublic", a + b);
    }

    @Test
    public void intComparison_isCorrect() {
        assertTrue(100 > 99);
    }
}