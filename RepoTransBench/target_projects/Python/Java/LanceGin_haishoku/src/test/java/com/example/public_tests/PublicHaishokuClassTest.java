package com.example.public_tests;

import com.example.haishoku.haishoku.Haishoku;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHaishokuClassTest {

    @Test
    public void testHaishokuMainColorDistinct() {
        Haishoku hs = new Haishoku("demo/demo_01.png");
        int[] main = hs.getMainColor();
        assertNotNull(main);
        assertEquals(3, main.length);
        for (int c : main) assertTrue(0 <= c && c <= 255);
        assertFalse(main[0] == 199 && main[1] == 146 && main[2] == 117);
    }
}