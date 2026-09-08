package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.barh.Barh;

public class TestBarhPublic {
    @Test
    public void testSimpleBarhDifferentData() {
        int[] y = {6, 1, 4};
        int[] x = {7, 8, 9};
        Barh.barh(y, x);
    }
}