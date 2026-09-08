package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;

import java.util.HashMap;
import java.util.Map;

public class PublicDiscoveryTest {

    @Test
    void testGetUrl() {
        HttpClient http = Mockito.mock(HttpClient.class);
        Map<String, String> result = new HashMap<>();
        result.put("findme", "foundval");
        Mockito.when(http.get(anyString())).thenReturn(result);
        Discovery discovery = new Discovery(http);

        assertEquals("foundval", discovery.getUrl("findme"));
    }

    @Test
    void testGetAppUrl() {
        HttpClient http = Mockito.mock(HttpClient.class);
        Map<String, String> result = new HashMap<>();
        result.put("lift", "found-lift");
        Mockito.when(http.get(anyString())).thenReturn(result);
        Discovery discovery = new Discovery(http);

        assertEquals("found-lift", discovery.getAppUrl("lift"));
    }
}