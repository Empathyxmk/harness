package com.example.activation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ActivationExamplePublicTest {
    @Test
    void testGetMessagePublic() {
        ActivationExample example = new ActivationExample();
        // Use different test data/message
        assertTrue(example.getMessage().contains("activated"));
    }
}