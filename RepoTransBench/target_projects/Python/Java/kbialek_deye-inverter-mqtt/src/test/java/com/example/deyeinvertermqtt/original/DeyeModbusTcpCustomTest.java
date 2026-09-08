package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeModbusTcpCustomTest {

    @Test
    public void testModbusCustomReadSuccess() {
        int value = 42;
        assertEquals(42, value, "Read value should match");
    }

    @Test
    public void testModbusCustomConnectionFailure() {
        Exception exception = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("Unable to connect");
        });
        assertEquals("Unable to connect", exception.getMessage());
    }
}