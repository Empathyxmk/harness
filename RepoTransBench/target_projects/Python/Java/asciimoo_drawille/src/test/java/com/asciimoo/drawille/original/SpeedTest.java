package com.asciimoo.drawille.original;

import com.asciimoo.drawille.Canvas;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SpeedTest {

    @Test
    void speedTestFrames() {
        Canvas c = new Canvas();
        int frames = 1000 * 10;
        int[][] sizes = {
            {0, 0},
            {10, 10},
            {20, 20},
            {20, 40},
            {40, 20},
            {40, 40},
            {100, 100}
        };

        for (int[] size : sizes) {
            int x = size[0], y = size[1];
            c.set(0, 0);
            for (int i = 0; i < y; i++) {
                c.set(x, i);
            }
            long start = System.nanoTime();
            for (int i = 0; i < frames; i++) {
                c.frame();
            }
            long end = System.nanoTime();
            System.out.printf("%dx%d\t%.4f\n", x, y, (end-start)*1.0e-9);
            c.clear();
        }
    }
}