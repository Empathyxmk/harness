package com.example.homu.original;

import com.example.homu.main.Main;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MainTest {

    @Test
    public void testProcessInputReverseExisting() {
        assertEquals("tset", Main.processInput("test"));
    }

    @Test
    public void testProcessInputPalindromeExisting() {
        assertEquals("abba", Main.processInput("abba"));
    }
}