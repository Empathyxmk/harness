package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.hist.Hist;

public class TestHist {
    @Test
    public void testSimpleHist() {
        int[] data = {1, 2, 2, 3};
        int[] binEdges = {1, 2, 3};
        Hist.hist(data, binEdges); // pass required binEdges argument
    }
}