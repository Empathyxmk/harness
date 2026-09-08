package com.betterprompt.original;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class BetterPromptTest {
    @Test
    public void testMetadata() {
        assertTrue(BetterPrompt.__version__ instanceof String);
        assertTrue(BetterPrompt.__author__ instanceof String);
        assertTrue(BetterPrompt.__copyright__ instanceof String);
        assertTrue(BetterPrompt.__license__ instanceof String);
        assertTrue(BetterPrompt.__all__.contains("getFromDictOrEnv"));
    }

    @Test
    public void testDummyOpenaiCompletionCreate() {
        Map<String, Object> result = BetterPrompt.DummyOpenAICompletion.create();
        assertNotNull(result);
        assertTrue(result.containsKey("choices"));
    }

    @Test
    public void testOpenaiCompletionStatic() {
        BetterPrompt.OpenAI.Completion oldCompletion = BetterPrompt.OpenAI.Completion;

        class DummyCompletion extends BetterPrompt.OpenAI.Completion {
            @Override
            public Map<String, Object> create(Object... args) {
                Map<String, Object> logprobs = new HashMap<>();
                logprobs.put("token_logprobs", Arrays.asList(0.5));
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
        try {
            Map<String, Object> res = BetterPrompt.OpenAI.Completion.create();
            Map<String, Object> choice = ((List<Map<String, Object>>) res.get("choices")).get(0);
            Map<String, Object> logprobs = (Map<String, Object>) choice.get("logprobs");
            List<Double> tokenLogprobs = (List<Double>) logprobs.get("token_logprobs");
            assertEquals(Arrays.asList(0.5), tokenLogprobs);
        } finally {
            BetterPrompt.OpenAI.Completion = oldCompletion;
        }
    }
}