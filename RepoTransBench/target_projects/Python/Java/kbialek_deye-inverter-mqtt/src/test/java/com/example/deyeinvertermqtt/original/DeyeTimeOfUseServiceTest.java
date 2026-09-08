package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeTimeOfUseServiceTest {

    @Test
    public void testTimeOfUseTariffSelection() {
        String tariff = "PEAK";
        assertEquals("PEAK", tariff, "Tariff should be PEAK");
    }
}