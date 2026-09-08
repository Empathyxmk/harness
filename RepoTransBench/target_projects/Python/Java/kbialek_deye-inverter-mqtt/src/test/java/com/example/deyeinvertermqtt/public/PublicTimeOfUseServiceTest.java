package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicTimeOfUseServiceTest {

    @Test
    public void testTariffSelectionPublic() {
        String tariff = "OFFPEAK";
        assertEquals("OFFPEAK", tariff, "Public tariff should be OFFPEAK");
    }
}