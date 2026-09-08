package com.example.aifunctions.original;

import com.example.aifunctions.*;
import org.junit.jupiter.api.*;
import org.mockito.ArgumentCaptor;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AIFunctionsOriginalTest {
    static AIClient originalAIClient;

    static class DummyAIClient implements AIClient {
        private final AIResponse dummyResponse;
        private final Map<String, Object> lastParams = new HashMap<>();
        private final String expectedModel;

        public DummyAIClient(AIResponse dummyResponse) {
            this.dummyResponse = dummyResponse;
            this.expectedModel = null;
        }
        public DummyAIClient(AIResponse dummyResponse, String expectedModel) {
            this.dummyResponse = dummyResponse;
            this.expectedModel = expectedModel;
        }

        @Override
        public AIResponse create(Map<String, Object> params) {
            if (expectedModel != null) {
                assertEquals(expectedModel, params.get("model"));
            }
            lastParams.putAll(params);
            return dummyResponse;
        }
    }

    @BeforeEach
    void backupAIClient() {
        originalAIClient = AIFunctions.aiClient;
    }
    @AfterEach
    void restoreAIClient() {
        AIFunctions.aiClient = originalAIClient;
    }

    @Test
    void test_ai_function_success() {
        AIResponse dummyResponse = new AIResponse("42");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse, "gpt-4");
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def add(a, b): return a + b",
                Arrays.asList("2", "40"),
                "Adds two numbers"
        );
        assertEquals("42", result);
    }

    @Test
    void test_ai_function_custom_model() {
        AIResponse dummyResponse = new AIResponse("7");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse, "gpt-3.5-turbo");
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def mul(a, b): return a * b",
                Arrays.asList("3", "4"),
                "Multiply two numbers",
                "gpt-3.5-turbo"
        );
        assertEquals("7", result);
    }

    @Test
    void test_ai_function_no_args() {
        AIResponse dummyResponse = new AIResponse("no args");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse);
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def f(): return None",
                new ArrayList<>(),
                "No-argument function"
        );
        assertEquals("no args", result);
    }

    @Test
    void test_ai_function_response_structure() {
        final Map<String, Object>[] capturedParams = new Map[1];

        AIFunctions.aiClient = params -> {
            capturedParams[0] = params;
            return new AIResponse("X");
        };

        AIFunctions.aiFunction("def f(x): return x", Arrays.asList("7"), "Echo integer");
        @SuppressWarnings("unchecked")
        List<Map<String, String>> messages = (List<Map<String, String>>) capturedParams[0].get("messages");
        Map<String, String> sysMsg = messages.get(0);
        assertEquals("system", sysMsg.get("role"));
        assertTrue(sysMsg.get("content").toLowerCase().contains("python function"));

        Map<String, String> userMsg = messages.get(1);
        assertEquals("user", userMsg.get("role"));
        assertEquals("7", userMsg.get("content"));
    }
}