package com.betterprompt.public_tests;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import org.mockito.MockedStatic;
import org.mockito.Mockito;

import java.util.*;

public class PublicBetterPromptTest {
    @Test
    public void testPublicCallOpenaiCustomModel() {
        List<Double> dummyLogprobs = Arrays.asList(-0.1, 2.5, -4.3);
        class DummyCompletion extends BetterPrompt.OpenAI.Completion {
            @Override
            public Map<String, Object> create(Object... args) {
                Map<String, Object> logprobs = new HashMap<>();
                logprobs.put("token_logprobs", dummyLogprobs);
                Map<String, Object> choice = new HashMap<>();
                choice.put("logprobs", logprobs);
                Map<String, Object> completion = new HashMap<>();
                completion.put("choices", Collections.singletonList(choice));
                return completion;
            }
            @Override
            public Map<String, Object> create(String prompt, String model, String apiKey) {
                assertEquals("public-model", model);
                return create();
            }
        }
        BetterPrompt.OpenAI.Completion = new DummyCompletion();
        List<Double> res = BetterPrompt.callOpenAI("sample prompt here", "public-model", "anypublickey");
        assertEquals(dummyLogprobs, res);
    }

    @Test
    public void testPublicCallOpenaiEnv() {
        List<Double> dummyLogprobs = Arrays.asList(7.0, 8.0);
        class DummyCompletion extends BetterPrompt.OpenAI.Completion {
            @Override
            public Map<String, Object> create(Object... args) {
                Map<String, Object> logprobs = new HashMap<>();
                logprobs.put("token_logprobs", dummyLogprobs);
                Map<String, Object> choice = new HashMap<>();
                choice.put("logprobs", logprobs);
                Map<String, Object> completion = new HashMap<>();
                completion.put("choices", Collections.singletonList(choice));
                return completion;
            }
            @Override
            public Map<String, Object> create(String prompt, String model, String apiKey) {
                return create();
            }
        }
        BetterPrompt.OpenAI.Completion = new DummyCompletion();
        try (MockedStatic<System> sysMock = Mockito.mockStatic(System.class)) {
            sysMock.when(() -> System.getenv("OPENAI_API_KEY")).thenReturn("public_env_key_test");
            List<Double> res = BetterPrompt.callOpenAI("prompt string");
            assertEquals(dummyLogprobs, res);
        }
    }

    @Test
    public void testPublicCalculatePerplexityDifferent() {
        List<Double> tokenLogprobs = Arrays.asList(-1.0, 0.0, 1.0, 2.0);
        double expected = Math.exp(-(-1.0 + 0.0 + 1.0 + 2.0) / 4.0);
        double actual = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(actual - expected) < 1e-8);
    }
}