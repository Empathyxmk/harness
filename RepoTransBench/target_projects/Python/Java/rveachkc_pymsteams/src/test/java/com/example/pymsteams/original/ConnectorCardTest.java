package com.example.pymsteams.original;

import com.example.pymsteams.CardSection;
import com.example.pymsteams.PotentialAction;
import com.example.pymsteams.ConnectorCard;
import com.example.pymsteams.TeamsWebhookException;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ConnectorCardTest {
    public static class MockHttpResponse {
        public int statusCode;
        public MockHttpResponse(int statusCode) { this.statusCode = statusCode; }
    }
    public static interface MockHttpClient {
        MockHttpResponse post(String url, Map<String, Object> payload);
    }

    @Test
    void testConnectorCardInitAndSummary() throws Exception {
        String url = "https://outlook.office.com/webhook/dummy_url";
        ConnectorCard c = new ConnectorCard(url);
        assertEquals(url, c.hookurl);
        c.text("Hello World");
        assertEquals("Hello World", c.payload.get("text"));
        c.summary("Summary");
        assertEquals("Summary", c.payload.get("summary"));
        c.title("A title here");
        assertEquals("A title here", c.payload.get("title"));
        c.color("123456");
        assertEquals("123456", c.payload.get("themeColor"));

        CardSection section = new CardSection();
        section.activityImage("https://i/image.png");
        assertEquals("https://i/image.png", section.payload.get("activityImage"));
        section.activityTitle("Do Something");
        assertEquals("Do Something", section.payload.get("activityTitle"));
        section.activitySubtitle("subtitle");
        assertEquals("subtitle", section.payload.get("activitySubtitle"));
        section.activityText("text activity");
        assertEquals("text activity", section.payload.get("activityText"));

        Map<String, Object> payload = c.payload;
        assertTrue(payload instanceof Map);
        ObjectMapper mapper = new ObjectMapper();
        String dumped = mapper.writeValueAsString(payload);
        assertTrue(dumped instanceof String);
    }

    @Test
    void testConnectorCardAddSection() {
        String url = "https://outlook.office.com/webhook/dummy_url";
        ConnectorCard c = new ConnectorCard(url);
        CardSection section = new CardSection();
        section.title("Section1 Title");
        c.addSection(section);
        assertTrue(c.payload.containsKey("sections"));
        List<Map<String, Object>> sections = (List<Map<String, Object>>) c.payload.get("sections");
        assertEquals("Section1 Title", sections.get(0).get("title"));
    }

    @Test
    void testConnectorCardAddPotentialAction() {
        String url = "https://outlook.office.com/webhook/dummy_url";
        ConnectorCard c = new ConnectorCard(url);
        PotentialAction pa = new PotentialAction("openUri");
        c.addPotentialAction(pa);
        assertTrue(c.payload.containsKey("potentialAction"));
        List<Map<String, Object>> pas = (List<Map<String, Object>>) c.payload.get("potentialAction");
        assertEquals("ActionCard", pas.get(0).get("@type"));
    }

    @Test
    void testConnectorCardSendRequestSuccess() {
        String url = "https://outlook.office.com/webhook/dummy_url";
        MockHttpClient client = (String u, Map<String, Object> p) -> new MockHttpResponse(200);
        ConnectorCard c = new ConnectorCard(url);
        c.text("posting");
        c.send(client); // should not throw
    }

    @Test
    void testConnectorCardSendRequestError() {
        String url = "https://outlook.office.com/webhook/dummy_url";
        MockHttpClient client = (String u, Map<String, Object> p) -> new MockHttpResponse(400);
        ConnectorCard c = new ConnectorCard(url);
        c.text("posting error");
        assertThrows(TeamsWebhookException.class, () -> {
            c.send(client);
        });
    }
}