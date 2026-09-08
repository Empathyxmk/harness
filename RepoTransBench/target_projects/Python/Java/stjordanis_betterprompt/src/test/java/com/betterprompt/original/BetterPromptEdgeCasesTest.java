package com.betterprompt.original;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import java.util.*;

public class BetterPromptEdgeCasesTest {
    @Test
    public void testGetFromDictOrEnvEmptyDictNoEnv() {
        String key = "TEST_MISSING_KEY";
        Map<String, String> map = new HashMap<>();
        try (MockedStatic<System> sysMock = Mockito.mockStatic(System.class)) {
            sysMock.when(() -> System.getenv(key)).thenReturn(null);
            Exception ex = assertThrows(IllegalArgumentException.class, () -> {
                BetterPrompt.getFromDictOrEnv(key, map);
            });
            assertTrue(ex.getMessage().contains(key));
        }
    }

    @Test
    public void testGetFromDictOrEnvNoneDictEnv() {
        String key = "ENV_ONLY_KEY";
        try (MockedStatic<System> sysMock = Mockito.mockStatic(System.class)) {
            sysMock.when(() -> System.getenv(key)).thenReturn("val");
            assertEquals("val", BetterPrompt.getFromDictOrEnv(key, null));
        }
    }

    @Test
    public void testGetFromDictOrEnvDictEmpty() {
        String key = "NO_DICT_KEY";
        Map<String, String> empty = new HashMap<>();
        try (MockedStatic<System> sysMock = Mockito.mockStatic(System.class)) {
            sysMock.when(() -> System.getenv(key)).thenReturn("from_env");
            assertEquals("from_env", BetterPrompt.getFromDictOrEnv(key, empty));
        }
    }

    @Test
    public void testOpenaiClassAndDummy() {
        Map<String, Object> result = BetterPrompt.OpenAI.Completion.create();
        assertNotNull(result);
        assertTrue(result.containsKey("choices"));
    }

    @Test
    public void testCallOpenaiApiKey() {
        List<Double> dummyLogprobs = Arrays.asList(0.4, 0.5, 0.6);

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
        List<Double> result = BetterPrompt.callOpenAI("prompt", "irrelevant", "explicit_key");
        assertEquals(dummyLogprobs, result);
    }

    @Test
    public void testCalculatePerplexityRegular() {
        List<Double> tokenLogprobs = Arrays.asList(0.0, -1.0, -2.0);
        double expected = Math.exp(-(0.0 + -1.0 + -2.0) / 3.0);
        double perplexity = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(perplexity - expected) < 1e-8);
    }

    @Test
    public void testCalculatePerplexityEmpty() {
        double result = BetterPrompt.calculatePerplexity(Collections.emptyList());
        assertTrue(Double.isInfinite(result));
    }
}