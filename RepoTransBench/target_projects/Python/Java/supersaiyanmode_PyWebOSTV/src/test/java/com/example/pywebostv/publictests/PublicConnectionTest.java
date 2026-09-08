package com.example.pywebostv.publictests;

import com.example.pywebostv.utils.FakeClient;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicConnectionTest {
    @Test
    public void testUniqueIdPublic() {
        FakeClient client = new FakeClient();
        String uid = "#87";
        Map<String, Object> payload = Map.of("val", "data");
        client.sendMessage("rsp", "urn", payload, uid);
        Map<String, Object> expected = Map.of(
                "id", "#87",
                "payload", payload,
                "type", "rsp",
                "uri", "urn"
        );
        client.assertSentMessage(expected);
    }

    // ... translate all public connection tests
}