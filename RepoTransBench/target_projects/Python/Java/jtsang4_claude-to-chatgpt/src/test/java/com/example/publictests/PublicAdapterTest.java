package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.util.*;

public class PublicAdapterTest {

    @Test
    public void testGetApiKeyFromHeadersPublic() {
        PublicTestClaudeAdapter ca = new PublicTestClaudeAdapter("http://another-url");
        Map<String, String> headers = new HashMap<>();
        headers.put("authorization", "Bearer another-key");
        assertEquals("another-key", ca.getApiKey(headers));
        ca.setClaudeApiKey("second-env-key");
        assertEquals("second-env-key", ca.getApiKey(new HashMap<>()));
    }

    @Test
    public void testConvertMessagesToPromptRolesPublic() {
        PublicTestClaudeAdapter ca = new PublicTestClaudeAdapter("public_url");
        List<Map<String, String>> messages = new ArrayList<>();
        messages.add(Map.of("role", "user", "content", "How are you?"));
        messages.add(Map.of("role", "assistant", "content", "I'm fine, thank you."));
        messages.add(Map.of("role", "system", "content", "System message here"));

        String prompt = ca.convertMessagesToPrompt(messages);
        assertTrue(prompt.contains("\n\nHuman: How are you?"));
        assertTrue(prompt.contains("\n\nAssistant: I'm fine, thank you."));
        assertTrue(prompt.contains("\n\nHuman: How are you?"));
        assertTrue(prompt.trim().endsWith("Assistant:"));
    }

    @Test
    public void testOpenaiToClaudeParamsAllPublic() {
        PublicTestClaudeAdapter ca = spy(new PublicTestClaudeAdapter());
        doReturn("DIFFERENT_PROMPT").when(ca).convertMessagesToPrompt(any());
        Map<String, Object> oai = new HashMap<>();
        oai.put("model", "gpt-4-0314");
        oai.put("messages", new ArrayList<>());
        oai.put("max_tokens", 1024);
        oai.put("stop", Arrays.asList("STOP_NOW"));
        oai.put("temperature", 0.55);
        oai.put("stream", false);
        ca.setModelMapEntry("gpt-4-0314", "claude-v1");

        Map<String, Object> result = ca.openaiToClaudeParams(oai);
        assertEquals("claude-v1", result.get("model"));
        assertEquals("DIFFERENT_PROMPT", result.get("prompt"));
        assertEquals(1024, result.get("max_tokens_to_sample"));
        assertEquals(Arrays.asList("STOP_NOW"), result.get("stop_sequences"));
        assertEquals(0.55, (Double)result.get("temperature"), 0.0001);
        assertFalse((Boolean)result.get("stream"));
    }

    @Test
    public void testOpenaiToClaudeParamsPartialPublic() {
        PublicTestClaudeAdapter ca = spy(new PublicTestClaudeAdapter());
        doReturn("ALT_PROMPT").when(ca).convertMessagesToPrompt(any());

        Map<String, Object> oai = new HashMap<>();
        oai.put("model", "absent-model");
        oai.put("messages", new ArrayList<>());

        ca.removeModelMapEntry("absent-model");
        Map<String, Object> result = ca.openaiToClaudeParams(oai);

        assertEquals("claude-2", result.get("model"));
        assertEquals("ALT_PROMPT", result.get("prompt"));
        assertEquals(100000, result.get("max_tokens_to_sample"));
    }

    @Test
    public void testClaudeToChatgptResponseStreamPublic() {
        PublicTestClaudeAdapter ca = spy(new PublicTestClaudeAdapter());
        String test_completion = "Different completion";
        String test_stop_reason = "max_tokens";
        ca.setNumTokens(10);
        Map<String, Object> response = ca.claudeToChatgptResponseStream(Map.of(
                "completion", test_completion,
                "stop_reason", test_stop_reason
        ));
        Map<String, Object> choice0 = ((List<Map<String, Object>>)response.get("choices")).get(0);
        Map<String, Object> delta = (Map<String, Object>)choice0.get("delta");
        assertEquals(test_completion, delta.get("content"));
        assertEquals(ca.getStopReasonMap().get(test_stop_reason), choice0.get("finish_reason"));
        Map<String, Object> usage = (Map<String, Object>)response.get("usage");
        assertEquals(10, usage.get("completion_tokens"));
    }

    @Test
    public void testClaudeToChatgptResponseNoStopPublic() {
        PublicTestClaudeAdapter ca = spy(new PublicTestClaudeAdapter());
        String test_completion = "A different completion text";
        ca.setNumTokens(7);

        Map<String, Object> response = ca.claudeToChatgptResponse(Map.of(
                "completion", test_completion
        ));
        Map<String, Object> choice0 = ((List<Map<String, Object>>)response.get("choices")).get(0);
        Map<String, Object> message = (Map<String, Object>)choice0.get("message");
        assertEquals(test_completion, message.get("content"));
        assertNull(choice0.get("finish_reason"));
        Map<String, Object> usage = (Map<String, Object>)response.get("usage");
        assertEquals(7, usage.get("completion_tokens"));
    }

    @Test
    public void testConvertMessagesToPromptCorrectFormatPublic() {
        PublicTestClaudeAdapter ca = new PublicTestClaudeAdapter();
        List<Map<String, String>> messages = new ArrayList<>();
        messages.add(Map.of("role", "user", "content", "What's up?"));
        String result = ca.convertMessagesToPrompt(messages);
        assertTrue(result.startsWith("\n\nHuman: What's up?") && result.endsWith("Assistant: "));
    }
}

class PublicTestClaudeAdapter extends com.example.original.TestClaudeAdapter {}