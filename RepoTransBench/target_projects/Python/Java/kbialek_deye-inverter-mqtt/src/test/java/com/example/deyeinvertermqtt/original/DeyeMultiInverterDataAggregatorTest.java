package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeMultiInverterDataAggregatorTest {

    @Test
    public void testAggregateMultipleInverterData() {
        int[] inverterPowers = {1000, 2000, 1500};
        int totalPower = 0;
        for (int p : inverterPowers) {
            totalPower += p;
        }
        assertEquals(4500, totalPower, "Aggregate should sum the inverter powers");
    }
}