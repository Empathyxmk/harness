package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultIterableTest {

    @Test
    void testIterableContent() {
        List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
        assertEquals(5, list.size());
        assertEquals(3, list.get(2).intValue());
    }

    @Test
    void testIterableSum() {
        List<Double> list = Arrays.asList(1.5, 2.0, 3.5);
        double sum = list.stream().mapToDouble(Double::doubleValue).sum();
        assertEquals(7.0, sum, 1e-8);
    }
}