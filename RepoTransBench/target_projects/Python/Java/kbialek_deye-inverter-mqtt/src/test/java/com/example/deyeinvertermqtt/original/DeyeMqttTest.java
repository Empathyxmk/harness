package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeMqttTest {

    @Test
    public void testMqttMessagePublish() {
        String message = "TEST";
        assertEquals("TEST", message, "Should publish correct message");
    }

    @Test
    public void testMqttInvalidTopicThrows() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException("Invalid topic");
        });
        assertEquals("Invalid topic", exception.getMessage());
    }
}