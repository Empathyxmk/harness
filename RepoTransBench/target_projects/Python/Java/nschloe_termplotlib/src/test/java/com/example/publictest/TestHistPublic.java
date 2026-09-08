package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.hist.Hist;

public class TestHistPublic {
    @Test
    public void testSimpleHistDiffData() {
        int[] data = {3, 6, 9, 3, 6, 9, 9};
        // Only pass data and bins param (no kwarg in Java)
        Hist.hist(data, 3);
    }

    @Test
    public void testHistLabelAndAscii() {
        int[] data = {7, 1, 6, 8, 7, 5, 5};
        Hist.hist(data, 2, "New Title", "Alternate X", "Alternate Y", true, true);
    }
}