package com.cloudconvert.original;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class SignedUrlTest {

    // Helper to simulate patching values (static for example)
    @BeforeEach
    void setup() {
        // Reset or mock global/static constants if needed
        // Not needed here as we directly pass the params
    }

    @Test
    void testGenerateSignedUrlWithPath() {
        String secretKey = "sekrit";
        String apiUrl = "https://api/";
        String result = SignedUrlUtil.generateSignedUrl(secretKey, apiUrl, "123", "test");
        assertTrue(result.startsWith("https://api/"), "URL should start with 'https://api/'");
    }

    @Test
    void testGenerateSignedUrlMissingKey() {
        String secretKey = null;
        String apiUrl = "https://api/";
        String result = SignedUrlUtil.generateSignedUrl(secretKey, apiUrl, "123", "test");
        assertNull(result, "If key missing then result should be null");
    }

    // ----------- Simulated implementation for demonstration purpose -----------
    static class SignedUrlUtil {
        // Simulate generate_signed_url with static/global values "patched" per test
        static String generateSignedUrl(String secretKey, String apiUrl, String jobId, String path) {
            if(secretKey == null || secretKey.isEmpty())
                return null;
            // Simulate URL scheme
            return apiUrl + "job/" + jobId + "/" + path + "?sig=dummy";
        }
    }
}