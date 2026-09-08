package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class SelectTest {
    @Test
    public void testSelectFirstTrue() {
        boolean[] arr = {false, true, false};
        int idx = -1;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i]) {
                idx = i;
                break;
            }
        }
        assertEquals(1, idx);
    }
}