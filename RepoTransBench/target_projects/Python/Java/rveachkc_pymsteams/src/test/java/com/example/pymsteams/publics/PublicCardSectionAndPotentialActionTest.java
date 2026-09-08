package com.example.pymsteams.publics;

import com.example.pymsteams.CardSection;
import com.example.pymsteams.PotentialAction;
import com.example.pymsteams.TeamsWebhookException;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicCardSectionAndPotentialActionTest {

    @Test
    void testCardSectionBasicPublic() {
        CardSection section = new CardSection();
        assertSame(section, section.title("Public Section Title"));
        assertEquals("Public Section Title", section.payload.get("title"));
        assertEquals("public activity", section.activityTitle("public activity").payload.get("activityTitle"));
        assertEquals("public subtitle", section.activitySubtitle("public subtitle").payload.get("activitySubtitle"));
        assertEquals("https://example.com/img.png", section.activityImage("https://example.com/img.png").payload.get("activityImage"));
        assertEquals("public text here", section.activityText("public text here").payload.get("activityText"));
        assertEquals("greetings", section.text("greetings").payload.get("text"));
        section.linkButton("Visit", "https://visit.com");
        List<Map<String, Object>> actions = (List<Map<String, Object>>) section.payload.get("potentialAction");
        assertEquals("Visit", actions.get(0).get("name"));
        assertEquals(false, section.disableMarkdown().payload.get("markdown"));
        assertEquals(true, section.enableMarkdown().payload.get("markdown"));
        Map<String, Object> dumped = section.dumpSection();
        assertNotNull(dumped);
        assertTrue(dumped instanceof Map);
    }

    @Test
    void testCardSectionAddFactAndAddImagePublic() {
        CardSection section = new CardSection();
        section.addFact("fact_one", "value_one");
        List<Map<String, String>> facts = (List<Map<String, String>>) section.payload.get("facts");
        assertEquals("fact_one", facts.get(0).get("name"));
        assertEquals("value_one", facts.get(0).get("value"));
        section.addFact("fact_two", "value_two");
        facts = (List<Map<String, String>>) section.payload.get("facts");
        assertEquals(2, facts.size());
        section.addImage("https://img-server.com/photo1.jpg", "photo title");
        List<Map<String, Object>> images = (List<Map<String, Object>>) section.payload.get("images");
        assertEquals("photo title", images.get(0).get("title"));
        section.addImage("https://img-server.com/photo2.jpg");
        images = (List<Map<String, Object>>) section.payload.get("images");
        assertFalse(images.get(1).containsKey("title"));
    }

    @Test
    void testCardSectionFactAndImageKeysPublic() {
        CardSection section = new CardSection();
        List<Map<String, String>> facts = new ArrayList<>();
        Map<String, String> fact = new HashMap<>();
        fact.put("name", "init_name");
        fact.put("value", "init_val");
        facts.add(fact);
        section.payload.put("facts", facts);
        section.addFact("another_name", "another_val");
        List<Map<String, String>> factsResult = (List<Map<String, String>>) section.payload.get("facts");
        assertEquals(2, factsResult.size());

        List<Map<String, Object>> images = new ArrayList<>();
        Map<String, Object> image = new HashMap<>();
        image.put("image", "img_obj");
        images.add(image);
        section.payload.put("images", images);
        section.addImage("more-img-url");
        List<Map<String, Object>> imagesResult = (List<Map<String, Object>>) section.payload.get("images");
        assertEquals(2, imagesResult.size());
    }

    @Test
    void testPotentialActionInputsAndActionsPublic() {
        PotentialAction pa = new PotentialAction("PublicAction");
        pa.addInput("TextInput", "pub_input", "Public Input Title", false);
        List<Map<String, Object>> inputs = (List<Map<String, Object>>) pa.payload.get("inputs");
        assertEquals(false, inputs.get(0).get("isMultiline"));

        pa.addInput("ChoiceInput", "pub_input2", "Public Choice Input", true);
        pa.addChoice("pub_display", "pub_value");
        inputs = (List<Map<String, Object>>) pa.payload.get("inputs");
        assertTrue(inputs.get(inputs.size() - 1).containsKey("choices"));

        pa.addAction("CustomActionType", "ActionPublic", Arrays.asList("https://example.org"));
        List<Map<String, Object>> actions = (List<Map<String, Object>>) pa.payload.get("actions");
        assertEquals("CustomActionType", actions.get(0).get("@type"));
        pa.addAction("secondtype", "publicaction", Arrays.asList("weburl"), "some body here");
        actions = (List<Map<String, Object>>) pa.payload.get("actions");
        assertEquals("some body here", actions.get(1).get("body"));
    }

    @Test
    void testPotentialActionAddOpenURIAndExceptionsPublic() {
        PotentialAction pa = new PotentialAction("testopen");
        List<Map<String, Object>> targets = new ArrayList<>();
        Map<String, Object> t = new HashMap<>();
        t.put("os", "mobile");
        t.put("uri", "https://other-url.com/");
        targets.add(t);
        PotentialAction res = pa.addOpenURI("OpenOther", targets);
        assertEquals(targets, res.payload.get("targets"));

        assertThrows(IllegalArgumentException.class, () -> {
            pa.addOpenURI("Failer", 12345);
        });
    }

    @Test
    void testPotentialActionDumpPublic() {
        PotentialAction pa = new PotentialAction("dumpPA");
        Map<String, Object> dumped = pa.dumpPotentialAction();
        assertNotNull(dumped);
        assertTrue(dumped instanceof Map);
    }

    @Test
    void testTeamsWebhookExceptionReprPublic() {
        TeamsWebhookException ex = new TeamsWebhookException("public fail");
        assertTrue(ex instanceof Exception);
        assertTrue(ex.getMessage().contains("public fail"));
    }
}