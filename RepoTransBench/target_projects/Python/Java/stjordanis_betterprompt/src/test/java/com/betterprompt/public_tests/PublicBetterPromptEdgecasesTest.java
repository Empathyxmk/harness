package com.betterprompt.public_tests;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import org.mockito.MockedStatic;
import org.mockito.Mockito;
import java.util.*;

public class PublicBetterPromptEdgecasesTest {

    @Test
    public void testPublicGetFromDictOrEnvMissing() {
        String key = "PUBLIC_ENV_KEY";
        Map<String, String> env = new HashMap<>();
        try (MockedStatic<System> mocked = Mockito.mockStatic(System.class)) {
            mocked.when(() -> System.getenv(key)).thenReturn(null);
            Exception e = assertThrows(IllegalArgumentException.class, () -> {
                BetterPrompt.getFromDictOrEnv(key, env);
            });
            assertTrue(e.getMessage().contains(key));
        }
    }

    @Test
    public void testPublicGetFromDictOrEnvDict() {
        String key = "DICT_ONLY_KEY";
        Map<String, String> d = new HashMap<>();
        d.put(key, "dict_value");
        try (MockedStatic<System> mocked = Mockito.mockStatic(System.class)) {
            mocked.when(() -> System.getenv(key)).thenReturn("env_value");
            assertEquals("dict_value", BetterPrompt.getFromDictOrEnv(key, d));
        }
    }

    @Test
    public void testPublicGetFromDictOrEnvEnv() {
        String key = "ENV_ONLY_KEY_PUBLIC";
        try (MockedStatic<System> mocked = Mockito.mockStatic(System.class)) {
            mocked.when(() -> System.getenv(key)).thenReturn("from_env_public");
            assertEquals("from_env_public", BetterPrompt.getFromDictOrEnv(key, null));
        }
    }

    @Test
    public void testPublicOpenaiClassDummy() {
        Map<String, Object> result = BetterPrompt.OpenAI.Completion.create();
        assertNotNull(result);
        assertTrue(result.containsKey("choices"));
    }

    @Test
    public void testPublicCallOpenaiApiKey() {
        List<Double> dummyLogprobs = Arrays.asList(1.23, -0.8, 3.14);
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
        List<Double> result = BetterPrompt.callOpenAI("test prompt", "irrelevant", "a_public_key");
        assertEquals(dummyLogprobs, result);
    }

    @Test
    public void testPublicCalculatePerplexityAllNegative() {
        List<Double> tokenLogprobs = Arrays.asList(-2.0, -4.0, -6.0);
        double expected = Math.exp(-(-2.0 + -4.0 + -6.0) / 3.0);
        double actual = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(actual - expected) < 1e-8);
    }

    @Test
    public void testPublicCalculatePerplexityEmpty() {
        double result = BetterPrompt.calculatePerplexity(Collections.emptyList());
        assertTrue(Double.isInfinite(result));
    }
}