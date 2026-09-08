package com.medium.sdk.original;

import com.medium.sdk.Client;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestClientExtra {

    @Test
    public void testClientInit() {
        Client c = new Client("12345");
        assertEquals("12345", c.token);
    }
}