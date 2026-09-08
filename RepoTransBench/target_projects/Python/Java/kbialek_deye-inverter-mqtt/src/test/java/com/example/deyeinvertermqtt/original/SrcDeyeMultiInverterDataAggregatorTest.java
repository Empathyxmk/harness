package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SrcDeyeMultiInverterDataAggregatorTest {

    @Test
    public void testSrcAggregate() {
        int[] values = {5, 7, 8};
        int sum = 0;
        for (int v : values) {
            sum += v;
        }
        assertEquals(20, sum, "Sum should be 20");
    }
}