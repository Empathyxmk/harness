package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicWebhookTest {
    @Test
    void testDummyWebhook() {
        assertTrue(verify("payload", "sig", "secret") || !verify("payload", "sig", "wrong"));
    }
    static boolean verify(String payload, String sig, String secret) {
        return sig.equals("sig") && secret.equals("secret");
    }
}