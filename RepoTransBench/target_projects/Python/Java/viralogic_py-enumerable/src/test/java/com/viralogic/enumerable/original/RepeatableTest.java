package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class RepeatableTest {

    @Test
    void testRepeatableEnumerables() {
        List<Integer> src = Arrays.asList(10, 20, 30);
        List<Integer> consumedOnce = new ArrayList<>(src);
        List<Integer> consumedTwice = new ArrayList<>(src);
        assertEquals(Arrays.asList(10,20,30), consumedOnce);
        assertEquals(Arrays.asList(10,20,30), consumedTwice);
    }
}