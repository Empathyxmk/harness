package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.plot.Plot;

public class TestScatter {
    @Test
    public void testSimpleScatter() {
        int[] x = {1,2,3};
        int[] y = {3,2,1};
        Plot.plot(y, x);
    }
}