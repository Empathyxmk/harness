package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicEndpointsTest {

    @Test
    public void testPublicDummyEndpoint() {
        assertEquals(4, 2 + 2);
    }

    @Test
    public void testPublicEndpointString() {
        assertTrue("myapiendpoint".contains("api"));
    }

    @Test
    public void testPublicEndpointNumeric() {
        assertEquals(27, 9 * 3);
    }
}