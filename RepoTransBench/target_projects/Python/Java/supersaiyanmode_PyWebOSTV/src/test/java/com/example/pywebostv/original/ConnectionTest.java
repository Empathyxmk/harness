package com.example.pywebostv.original;

import com.example.pywebostv.utils.FakeClient;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;

public class ConnectionTest {

    @Test
    public void testUniqueId() {
        FakeClient client = new FakeClient();
        String uid = "!23";
        Map<String, Object> payload = Map.of("item", "payload");
        client.sendMessage("req", "uri", payload, uid);
        Map<String, Object> expected = new HashMap<>();
        expected.put("id", "!23");
        expected.put("payload", payload);
        expected.put("type", "req");
        expected.put("uri", "uri");
        client.assertSentMessage(expected);
    }

    // ... and so on for each major test, matching logic and edge cases.

}