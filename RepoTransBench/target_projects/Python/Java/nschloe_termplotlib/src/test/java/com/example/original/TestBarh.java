package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.barh.Barh;

public class TestBarh {
    @Test
    public void testSimpleBarh() {
        int[] y = {3, 2, 5};
        int[] x = {1, 2, 3};
        Barh.barh(y, x);
    }
}