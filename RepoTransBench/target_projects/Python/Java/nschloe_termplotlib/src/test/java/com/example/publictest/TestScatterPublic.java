package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.plot.Plot;

public class TestScatterPublic {
    @Test
    public void testSimpleScatterDifferentData() {
        int[] x = {4, 5, 6};
        int[] y = {6, 5, 4};
        Plot.plot(y, x);
    }
}