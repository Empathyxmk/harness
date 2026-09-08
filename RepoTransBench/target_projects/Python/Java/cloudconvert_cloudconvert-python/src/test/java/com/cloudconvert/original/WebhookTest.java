package com.cloudconvert.original;

import org.junit.jupiter.api.Test;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import static org.junit.jupiter.api.Assertions.*;

class WebhookTest {

    static class WebhookUtil {
        public static boolean verify(String payload, String sig, String secret) {
            try {
                Mac hmacSha256 = Mac.getInstance("HmacSHA256");
                hmacSha256.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"));
                byte[] hash = hmacSha256.doFinal(payload.getBytes());
                String expected = bytesToHex(hash);
                return expected.equals(sig);
            } catch (Exception ex) {
                return false;
            }
        }

        private static String bytesToHex(byte[] bytes) {
            StringBuilder sb = new StringBuilder();
            for (byte b : bytes) sb.append(String.format("%02x", b));
            return sb.toString();
        }
    }

    @Test
    void testWebhookValidSignature() throws Exception {
        String payload = "data";
        String secret = "secret";
        Mac hmac = Mac.getInstance("HmacSHA256");
        hmac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"));
        String expectedSig = toHex(hmac.doFinal(payload.getBytes()));
        assertTrue(WebhookUtil.verify(payload, expectedSig, secret));
    }

    @Test
    void testWebhookInvalidSignature() {
        String payload = "data";
        String secret = "secret";
        assertFalse(WebhookUtil.verify(payload, "abc", secret));
    }

    @Test
    void testWebhookEmptyPayload() throws Exception {
        String payload = "";
        String secret = "secret";
        Mac hmac = Mac.getInstance("HmacSHA256");
        hmac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"));
        String expectedSig = toHex(hmac.doFinal(payload.getBytes()));
        assertTrue(WebhookUtil.verify(payload, expectedSig, secret));
    }

    @Test
    void testWebhookWrongSecret() throws Exception {
        String payload = "data";
        String secret = "right";
        String wrongSecret = "wrong";
        Mac hmac = Mac.getInstance("HmacSHA256");
        hmac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"));
        String correctSig = toHex(hmac.doFinal(payload.getBytes()));
        assertFalse(WebhookUtil.verify(payload, correctSig, wrongSecret));
    }

    private static String toHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) sb.append(String.format("%02x", b));
        return sb.toString();
    }
}