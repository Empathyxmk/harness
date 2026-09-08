package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.plot.Plot;

public class TestPlot {
    @Test
    public void testSimplePlot() {
        int[] y = {2, 3, 1};
        int[] x = {1, 2, 3};
        Plot.plot(y, x);
    }
}