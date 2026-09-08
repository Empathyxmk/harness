package com.example.public_tests;

import com.example.haishoku.haishoku.Haishoku;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHaishokuTest {

    @Test
    public void testHaishokuGetPalettePublic() {
        Haishoku hs = new Haishoku("demo/demo_01.png");
        int[][] palette = hs.getPalette();
        assertEquals(6, palette.length);
        for (int[] color : palette) {
            assertNotNull(color);
            assertEquals(3, color.length);
        }
    }
}