package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.plot.Plot;

public class TestPlotPublic {
    @Test
    public void testSimplePlotDifferentData() {
        int[] y = {0, 4, 2};
        int[] x = {10, 15, 20};
        Plot.plot(y, x);
    }
}