package com.loong.componentbase;

import org.junit.Test;

import static org.junit.Assert.*;

public class ExampleUnitPublicTest {
    @Test
    public void subtraction_isCorrect() {
        assertEquals(2, 5 - 3);
    }

    @Test
    public void multiplication_isCorrect() {
        assertEquals(15, 3 * 5);
    }
}