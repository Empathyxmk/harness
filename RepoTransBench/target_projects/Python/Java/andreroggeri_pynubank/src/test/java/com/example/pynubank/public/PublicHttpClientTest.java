package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.util.Map;
import java.util.HashMap;

public class PublicHttpClientTest {

    @Test
    void testGet() {
        HttpClient cli = spy(new HttpClient());
        Map<String, Object> json = new HashMap<>();
        json.put("pubkey", 777);
        DummyResponse resp = new DummyResponse(200, "public-url", json, null);
        doReturn(resp).when(cli).rawGet(anyString());
        Map<String, Object> result = cli.get("public-url");
        assertEquals(777, result.get("pubkey"));
    }

    @Test
    void testPost() {
        HttpClient cli = spy(new HttpClient());
        Map<String, Object> json = new HashMap<>();
        json.put("pubkey", 888);
        DummyResponse resp = new DummyResponse(200, "public-url", json, null);
        doReturn(resp).when(cli).rawPost(anyString(), any());
        Map<String, Object> result = cli.post("public-url", new HashMap<>());
        assertEquals(888, result.get("pubkey"));
    }
}