package com.example.ws;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class WSExamplePublicTest {
    @Test
    void testWSCallPublic() {
        WSExample ws = new WSExample();
        String result = ws.call();
        assertNotNull(result);
        assertFalse(result.isEmpty());
    }
}