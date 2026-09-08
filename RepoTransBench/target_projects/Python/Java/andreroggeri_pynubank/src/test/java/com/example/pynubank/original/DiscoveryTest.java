package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;

import java.util.HashMap;
import java.util.Map;

public class DiscoveryTest {

    private Discovery buildDiscovery() {
        HttpClient http = Mockito.mock(HttpClient.class);
        return new Discovery(http);
    }

    @Test
    void testGetUnexistentUrl() {
        HttpClient http = Mockito.mock(HttpClient.class);
        Map<String, String> proxyReturn = new HashMap<>();
        Mockito.when(http.get(anyString())).thenReturn(proxyReturn);
        Discovery discovery = new Discovery(http);
        assertThrows(NuException.class, () -> discovery.getUrl("some-url"));
    }

    @Test
    void testGetUrl() {
        HttpClient http = Mockito.mock(HttpClient.class);
        Map<String, String> proxyReturn = new HashMap<>();
        proxyReturn.put("token", "value");
        Mockito.when(http.get(anyString())).thenReturn(proxyReturn);
        Discovery discovery = new Discovery(http);
        assertEquals("value", discovery.getUrl("token"));
    }

    @Test
    void testGetAppUrl() {
        HttpClient http = Mockito.mock(HttpClient.class);
        Map<String, String> proxyReturn = new HashMap<>();
        proxyReturn.put("lift", "app-value");
        Mockito.when(http.get(anyString())).thenReturn(proxyReturn);
        Discovery discovery = new Discovery(http);
        assertEquals("app-value", discovery.getAppUrl("lift"));
    }

    @Test
    void testIsAliveIfNubankServerIsUp() {
        HttpClient http = new HttpClient() {
            @Override
            public DummyResponse rawGet(String url) {
                return new DummyResponse(200, url);
            }
        };
        assertTrue(http.isAlive());
    }

    @Test
    void testIsAliveIfNubankServerIsDown() {
        HttpClient http = new HttpClient() {
            @Override
            public DummyResponse rawGet(String url) {
                return new DummyResponse(404, url);
            }
        };
        assertFalse(http.isAlive());
    }
}