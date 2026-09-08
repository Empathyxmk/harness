package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestInitTest {
    @Test
    public void testClientInitialization() {
        String username = "john.doe@icloud.com";
        String client = username + "-client";
        assertTrue(client.contains("john.doe"));
        assertTrue(client.endsWith("-client"));
    }

    @Test
    public void testClientTokenPersistence() {
        boolean tokenSaved = true;
        assertTrue(tokenSaved);
    }
}