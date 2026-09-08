package com.loong.share;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleUnitPublicTest {
    @Test
    public void divide_isCorrect() {
        assertEquals(4, 8 / 2);
    }

    @Test
    public void stringStartsWith_isCorrect() {
        assertTrue("ShareTesting".startsWith("Share"));
    }
}