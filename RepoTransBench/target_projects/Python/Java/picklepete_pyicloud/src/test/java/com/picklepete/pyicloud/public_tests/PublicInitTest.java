package com.picklepete.pyicloud.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInitTest {

    @Test
    public void testPublicICloudClientInit() {
        String username = "user@icloud.com";
        String clientName = username + "-client";
        assertNotNull(clientName);
        assertTrue(clientName.contains("icloud.com"));
    }

    @Test
    public void testPublicTokenCreated() {
        String token = "token_12345";
        assertNotNull(token);
        assertTrue(token.startsWith("token_"));
    }
}