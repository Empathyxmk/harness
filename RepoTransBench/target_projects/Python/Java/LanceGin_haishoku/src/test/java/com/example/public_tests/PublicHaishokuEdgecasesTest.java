package com.example.public_tests;

import com.example.haishoku.alg.Alg;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHaishokuEdgecasesTest {

    @Test
    public void testRgb2hlsBoundary() {
        int[] black = {0, 0, 0};
        int[] white = {255, 255, 255};
        int[] resBlack = Alg.rgb2hls(black);
        int[] resWhite = Alg.rgb2hls(white);
        assertArrayEquals(new int[] {0, 0, 0}, resBlack);
        assertArrayEquals(new int[] {0, 255, 0}, resWhite);
    }
}