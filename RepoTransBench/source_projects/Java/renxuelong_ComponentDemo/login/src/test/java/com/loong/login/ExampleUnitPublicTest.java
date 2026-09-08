package com.loong.login;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleUnitPublicTest {
    @Test
    public void multiply_isCorrect() {
        assertEquals(30, 5 * 6);
    }

    @Test
    public void stringNotEquals_isCorrect() {
        assertNotEquals("login", "public_login");
    }
}