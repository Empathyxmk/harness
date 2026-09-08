package com.example.pymsteams.original;

import com.example.pymsteams.CardSection;
import com.example.pymsteams.PotentialAction;
import com.example.pymsteams.TeamsWebhookException;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class CardSectionAndPotentialActionTest {

    @Test
    void testCardSectionBasic() {
        CardSection section = new CardSection();
        assertSame(section, section.title("title text"));
        assertEquals("title text", section.payload.get("title"));
        assertEquals("activity", section.activityTitle("activity").payload.get("activityTitle"));
        assertEquals("subtitle", section.activitySubtitle("subtitle").payload.get("activitySubtitle"));
        assertEquals("http://image.png", section.activityImage("http://image.png").payload.get("activityImage"));
        assertEquals("text here", section.activityText("text here").payload.get("activityText"));
        assertEquals("hello", section.text("hello").payload.get("text"));
        section.linkButton("Go", "http://go.com");
        List<Map<String, Object>> actions = (List<Map<String, Object>>) section.payload.get("potentialAction");
        assertEquals("Go", actions.get(0).get("name"));
        assertEquals(false, section.disableMarkdown().payload.get("markdown"));
        assertEquals(true, section.enableMarkdown().payload.get("markdown"));
        Map<String, Object> dumped = section.dumpSection();
        assertNotNull(dumped);
        assertTrue(dumped instanceof Map);
    }

    @Test
    void testCardSectionAddFactAndAddImage() {
        CardSection section = new CardSection();
        section.addFact("f1", "v1");
        List<Map<String, String>> facts = (List<Map<String, String>>) section.payload.get("facts");
        assertEquals(Arrays.asList(Map.of("name", "f1", "value", "v1")), facts);
        section.addFact("f2", "v2");
        assertEquals(2, ((List<?>) section.payload.get("facts")).size());
        section.addImage("http://img.com/img.jpg", "image1");
        List<Map<String, Object>> images = (List<Map<String, Object>>) section.payload.get("images");
        assertEquals("image1", images.get(0).get("title"));
        section.addImage("http://img.com/img2.jpg");
        images = (List<Map<String, Object>>) section.payload.get("images");
        assertFalse(images.get(1).containsKey("title"));
    }

    @Test
    void testCardSectionFactAndImageKeys() {
        CardSection section = new CardSection();
        // manually seed facts and images for test
        List<Map<String, String>> facts = new ArrayList<>();
        facts.add(new HashMap<>(Map.of("name", "start", "value", "val")));
        section.payload.put("facts", facts);
        section.addFact("foo", "bar");
        assertEquals(2, ((List<?>) section.payload.get("facts")).size());

        List<Map<String, Object>> images = new ArrayList<>();
        images.add(new HashMap<>(Map.of("image", "test")));
        section.payload.put("images", images);
        section.addImage("img-url");
        assertEquals(2, ((List<?>) section.payload.get("images")).size());
    }

    @Test
    void testPotentialActionInputsAndActions() {
        PotentialAction pa = new PotentialAction("TestAction");
        pa.addInput("TextInput", "inputid", "My Title", true);
        List<Map<String, Object>> inputs = (List<Map<String, Object>>) pa.payload.get("inputs");
        assertEquals(true, inputs.get(0).get("isMultiline"));

        pa.addInput("ChoiceInput", "input2", "Another", false);
        pa.addChoice("display", "value");
        inputs = (List<Map<String, Object>>) pa.payload.get("inputs");
        assertTrue(inputs.get(inputs.size() - 1).containsKey("choices"));

        pa.addAction("ActionType", "ActionName", Arrays.asList("http://example.com"));
        List<Map<String, Object>> actions = (List<Map<String, Object>>) pa.payload.get("actions");
        assertEquals("ActionType", actions.get(0).get("@type"));
        pa.addAction("type", "name", Arrays.asList("url"), "body here");
        actions = (List<Map<String, Object>>) pa.payload.get("actions");
        assertEquals("body here", actions.get(1).get("body"));
    }

    @Test
    void testPotentialActionAddOpenURIAndExceptions() {
        PotentialAction pa = new PotentialAction("opentest");
        List<Map<String, Object>> targets = new ArrayList<>();
        Map<String, Object> t = new HashMap<>();
        t.put("os", "default");
        t.put("uri", "https://foo.bar/");
        targets.add(t);
        PotentialAction res = pa.addOpenURI("OpenName", targets);
        assertEquals(targets, res.payload.get("targets"));

        assertThrows(IllegalArgumentException.class, () -> {
            pa.addOpenURI("Broken", "notalist");
        });
    }

    @Test
    void testPotentialActionDump() {
        PotentialAction pa = new PotentialAction("dumpTest");
        Map<String, Object> dumped = pa.dumpPotentialAction();
        assertNotNull(dumped);
        assertTrue(dumped instanceof Map);
    }

    @Test
    void testTeamsWebhookExceptionRepr() {
        TeamsWebhookException ex = new TeamsWebhookException("fail");
        assertTrue(ex instanceof Exception);
        assertTrue(ex.getMessage().contains("fail"));
    }
}