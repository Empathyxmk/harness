package com.example.pymsteams.publics;

import com.example.pymsteams.CardSection;
import com.example.pymsteams.PotentialAction;
import com.example.pymsteams.ConnectorCard;
import com.example.pymsteams.TeamsWebhookException;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class PublicConnectorCardTest {
    public static class MockHttpResponse {
        public int statusCode;
        public MockHttpResponse(int statusCode) { this.statusCode = statusCode; }
    }
    public static interface MockHttpClient {
        MockHttpResponse post(String url, Map<String, Object> payload);
    }

    @Test
    void testConnectorCardInitAndSummaryPublic() throws Exception {
        String url = "https://somedomain.com/webhook/unique_id";
        ConnectorCard c = new ConnectorCard(url);
        assertEquals(url, c.hookurl);
        c.text("Public Hello Text");
        assertEquals("Public Hello Text", c.payload.get("text"));
        c.summary("Public Summary");
        assertEquals("Public Summary", c.payload.get("summary"));
        c.title("Some Public Title");
        assertEquals("Some Public Title", c.payload.get("title"));
        c.color("ABCDEF");
        assertEquals("ABCDEF", c.payload.get("themeColor"));

        CardSection section = new CardSection();
        section.activityImage("https://images.example.com/pic.png");
        assertEquals("https://images.example.com/pic.png", section.payload.get("activityImage"));
        section.activityTitle("Demo Action");
        assertEquals("Demo Action", section.payload.get("activityTitle"));
        section.activitySubtitle("demo subtitle");
        assertEquals("demo subtitle", section.payload.get("activitySubtitle"));
        section.activityText("some public activity text");
        assertEquals("some public activity text", section.payload.get("activityText"));

        Map<String, Object> payload = c.payload;
        assertTrue(payload instanceof Map);

        ObjectMapper mapper = new ObjectMapper();
        String dumped = mapper.writeValueAsString(payload);
        assertTrue(dumped instanceof String);
    }

    @Test
    void testConnectorCardAddSectionPublic() {
        String url = "https://somedomain.com/webhook/other_id";
        ConnectorCard c = new ConnectorCard(url);
        CardSection section = new CardSection();
        section.title("Public Section2 Title");
        c.addSection(section);
        assertTrue(c.payload.containsKey("sections"));
        List<Map<String, Object>> sections = (List<Map<String, Object>>) c.payload.get("sections");
        assertEquals("Public Section2 Title", sections.get(0).get("title"));
    }

    @Test
    void testConnectorCardAddPotentialActionPublic() {
        String url = "https://somedomain.com/webhook/pa_id";
        ConnectorCard c = new ConnectorCard(url);
        PotentialAction pa = new PotentialAction("otherOpenUri");
        c.addPotentialAction(pa);
        assertTrue(c.payload.containsKey("potentialAction"));
        List<Map<String, Object>> pas = (List<Map<String, Object>>) c.payload.get("potentialAction");
        assertEquals("ActionCard", pas.get(0).get("@type"));
    }

    @Test
    void testConnectorCardSendRequestPublicSuccess() {
        String url = "https://somedomain.com/webhook/send_id";
        MockHttpClient client = (String u, Map<String, Object> p) -> new MockHttpResponse(201);
        ConnectorCard c = new ConnectorCard(url);
        c.text("another post");
        c.send(client); // should not throw
    }

    @Test
    void testConnectorCardSendRequestErrorPublic() {
        String url = "https://somedomain.com/webhook/send_error";
        MockHttpClient client = (String u, Map<String, Object> p) -> new MockHttpResponse(404);
        ConnectorCard c = new ConnectorCard(url);
        c.text("posting error test");
        assertThrows(TeamsWebhookException.class, () -> {
            c.send(client);
        });
    }
}