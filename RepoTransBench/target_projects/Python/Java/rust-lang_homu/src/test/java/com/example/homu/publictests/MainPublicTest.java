package com.example.homu.publictests;

import com.example.homu.main.Main;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MainPublicTest {

    @Test
    public void testProcessInputReverse() {
        assertEquals("ahpla", Main.processInput("alpha"));
    }

    @Test
    public void testProcessInputPalindrome() {
        assertEquals("noon", Main.processInput("noon"));
    }
}