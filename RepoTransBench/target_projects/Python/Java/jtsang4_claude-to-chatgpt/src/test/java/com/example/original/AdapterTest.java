package com.example.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class AdapterTest {

    private TestClaudeAdapter ca;

    @BeforeEach
    public void setup() {
        ca = new TestClaudeAdapter();
    }

    @Test
    public void testGetApiKeyFromHeaders() {
        ca = new TestClaudeAdapter("http://test-url");
        // Case: Authorization header present
        Map<String, String> headers = new HashMap<>();
        headers.put("authorization", "Bearer secret-key");
        assertEquals("secret-key", ca.getApiKey(headers));
        // Case: Authorization header missing
        ca.setClaudeApiKey("backup-from-env");
        assertEquals("backup-from-env", ca.getApiKey(new HashMap<>()));
    }

    @Test
    public void testConvertMessagesToPromptRoles() {
        ca = new TestClaudeAdapter("url");
        List<Map<String, String>> messages = new ArrayList<>();
        messages.add(Map.of("role", "user", "content", "hello"));
        messages.add(Map.of("role", "assistant", "content", "hi!"));
        messages.add(Map.of("role", "system", "content", "sysmsg"));

        String prompt = ca.convertMessagesToPrompt(messages);
        assertTrue(prompt.contains("\n\nHuman: hello"));
        assertTrue(prompt.contains("\n\nAssistant: hi!"));
        assertTrue(prompt.contains("\n\nHuman: hello"));
        assertTrue(prompt.trim().endsWith("Assistant:"));
    }

    @Test
    public void testOpenaiToClaudeParamsAll() {
        ca = spy(new TestClaudeAdapter());
        doReturn("PROMPT!").when(ca).convertMessagesToPrompt(any());

        Map<String, Object> oai = new HashMap<>();
        oai.put("model", "gpt-3.5-turbo-0613");
        oai.put("messages", new ArrayList<>());
        oai.put("max_tokens", 512);
        oai.put("stop", Arrays.asList("THE END"));
        oai.put("temperature", 0.3);
        oai.put("stream", true);

        ca.setModelMapEntry("gpt-3.5-turbo-0613", "claude-2");
        Map<String, Object> result = ca.openaiToClaudeParams(oai);
        assertEquals("claude-2", result.get("model"));
        assertEquals("PROMPT!", result.get("prompt"));
        assertEquals(512, result.get("max_tokens_to_sample"));
        assertEquals(Arrays.asList("THE END"), result.get("stop_sequences"));
        assertEquals(0.3, (Double)result.get("temperature"), 0.0001);
        assertTrue((Boolean) result.get("stream"));
    }

    @Test
    public void testOpenaiToClaudeParamsPartial() {
        ca = spy(new TestClaudeAdapter());
        doReturn("PROMPT!").when(ca).convertMessagesToPrompt(any());

        Map<String, Object> oai = new HashMap<>();
        oai.put("model", "non-existent");
        oai.put("messages", new ArrayList<>());

        ca.removeModelMapEntry("non-existent");
        Map<String, Object> result = ca.openaiToClaudeParams(oai);
        assertEquals("claude-2", result.get("model"));
        assertEquals("PROMPT!", result.get("prompt"));
        assertEquals(100000, result.get("max_tokens_to_sample"));
    }

    @Test
    public void testClaudeToChatgptResponseStream() {
        ca = spy(new TestClaudeAdapter());
        String test_completion = "Some completion text";
        String test_stop_reason = "stop_sequence";
        ca.setNumTokens(5);

        Map<String, Object> response = ca.claudeToChatgptResponseStream(Map.of(
                "completion", test_completion, 
                "stop_reason", test_stop_reason
        ));
        Map<String, Object> choice0 = ((List<Map<String, Object>>)response.get("choices")).get(0);
        Map<String, Object> delta = (Map<String, Object>)choice0.get("delta");
        assertEquals(test_completion, delta.get("content"));
        assertEquals(ca.getStopReasonMap().get(test_stop_reason), choice0.get("finish_reason"));
        Map<String, Object> usage = (Map<String, Object>)response.get("usage");
        assertEquals(5, usage.get("completion_tokens"));
    }

    @Test
    public void testClaudeToChatgptResponseNoStop() {
        ca = spy(new TestClaudeAdapter());
        String test_completion = "Some completion text";
        ca.setNumTokens(5);

        Map<String, Object> response = ca.claudeToChatgptResponse(Map.of(
                "completion", test_completion
        ));
        Map<String, Object> choice0 = ((List<Map<String, Object>>)response.get("choices")).get(0);
        Map<String, Object> message = (Map<String, Object>)choice0.get("message");
        assertEquals(test_completion, message.get("content"));
        assertNull(choice0.get("finish_reason"));
        Map<String, Object> usage = (Map<String, Object>)response.get("usage");
        assertEquals(5, usage.get("completion_tokens"));
    }

    @Test
    public void testConvertMessagesToPromptCorrectFormat() {
        ca = new TestClaudeAdapter();
        List<Map<String, String>> messages = new ArrayList<>();
        messages.add(Map.of("role", "user", "content", "hi"));
        String result = ca.convertMessagesToPrompt(messages);
        assertTrue(result.startsWith("\n\nHuman: hi") && result.endsWith("Assistant: "));
    }
}

// Your minimal test double implementation for the purpose of testing logic
class TestClaudeAdapter {
    private String apiUrl = "";
    private String claudeApiKey = null;
    private Map<String, String> modelMap = new HashMap<>();
    private int numTokensFixed = -1;

    public TestClaudeAdapter() {}
    public TestClaudeAdapter(String url) { this.apiUrl=url; }

    public void setClaudeApiKey(String key) { this.claudeApiKey = key; }
    public void setModelMapEntry(String k, String v) { modelMap.put(k, v); }
    public void removeModelMapEntry(String k) { modelMap.remove(k); }
    public void setNumTokens(int n) { numTokensFixed = n; }
    public Map<String, String> getStopReasonMap() {
        return Map.of("stop_sequence","stop","max_tokens","length");
    }

    // Simulate: get_api_key
    public String getApiKey(Map<String, String> headers) {
        String header = headers.getOrDefault("authorization", null);
        if (header != null && header.startsWith("Bearer ")) {
            return header.substring("Bearer ".length());
        }
        if (claudeApiKey != null) return claudeApiKey;
        return null;
    }

    // Simulate: convert_messages_to_prompt
    public String convertMessagesToPrompt(List<Map<String, String>> messages) {
        StringBuilder sb = new StringBuilder();
        for (Map<String, String> m : messages) {
            String role = m.get("role");
            String content = m.get("content");
            if ("user".equals(role) || "system".equals(role))
                sb.append("\n\nHuman: ").append(content);
            else if ("assistant".equals(role))
                sb.append("\n\nAssistant: ").append(content);
        }
        sb.append("Assistant:");
        return sb.toString();
    }

    // Simulate: openai_to_claude_params
    public Map<String, Object> openaiToClaudeParams(Map<String, Object> oai) {
        String model = (String)oai.getOrDefault("model", "");
        String prompt = convertMessagesToPrompt(
            (List<Map<String, String>>) oai.getOrDefault("messages", new ArrayList<>()));
        int maxTokens = (int)oai.getOrDefault("max_tokens", 100000);
        Object stop = oai.getOrDefault("stop", Arrays.asList());
        double temp = oai.containsKey("temperature") ? ((Number)oai.get("temperature")).doubleValue() : 1.0;
        boolean stream = oai.containsKey("stream") ? (Boolean)oai.get("stream") : false;
        String mappedModel = modelMap.getOrDefault(model, "claude-2");

        return new HashMap<>(Map.of(
            "model", mappedModel,
            "prompt", prompt,
            "max_tokens_to_sample", maxTokens,
            "stop_sequences", stop,
            "temperature", temp,
            "stream", stream
        ));
    }

    // Simulate: stream response
    public Map<String, Object> claudeToChatgptResponseStream(Map<String, Object> data) {
        String completion = (String)data.get("completion");
        String stopReason = (String)data.get("stop_reason");
        Map<String, Object> delta = Map.of("content", completion);
        Map<String, Object> c = Map.of(
            "delta", delta,
            "finish_reason", getStopReasonMap().get(stopReason)
        );
        return Map.of(
            "choices", List.of(c),
            "usage", Map.of("completion_tokens", getNumTokens(completion))
        );
    }

    // Simulate: non-stream response
    public Map<String, Object> claudeToChatgptResponse(Map<String, Object> data) {
        String completion = (String)data.get("completion");
        Map<String, Object> message = Map.of("content", completion);
        Map<String, Object> c = Map.of(
            "message", message,
            "finish_reason", null
        );
        return Map.of(
            "choices", List.of(c),
            "usage", Map.of("completion_tokens", getNumTokens(completion))
        );
    }

    // Used in place of monkeypatching num_tokens_from_string
    private int getNumTokens(String input) {
        return (numTokensFixed != -1) ? numTokensFixed : 
                (input == null ? 0 : input.length());
    }
}