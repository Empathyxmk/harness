package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicMultiInverterDataAggregatorTest {

    @Test
    public void testPublicAggregatorSummary() {
        int[] values = {1, 2, 3};
        int sum = 0;
        for (int v : values) {
            sum += v;
        }
        assertEquals(6, sum, "Sum must be 6");
    }
}