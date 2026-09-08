package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicMockHttpClientTest {
    @Test
    void testGetInvalidUrlShouldThrowException() {
        MockHttpClient client = new MockHttpClient();
        assertThrows(NuException.class, () -> client.get("nonexistent.url"));
    }

    @Test
    void testPostInvalidUrlShouldThrowException() {
        MockHttpClient client = new MockHttpClient();
        assertThrows(NuException.class, () -> client.post("nonexistent.url", null));
    }
}