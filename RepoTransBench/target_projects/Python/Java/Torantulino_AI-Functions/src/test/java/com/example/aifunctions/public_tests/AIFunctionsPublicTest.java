package com.example.aifunctions.public_tests;

import com.example.aifunctions.*;

import org.junit.jupiter.api.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class AIFunctionsPublicTest {
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
    void test_public_ai_function_success() {
        AIResponse dummyResponse = new AIResponse("17");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse, "gpt-4");
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def subtract(a, b): return a - b",
                Arrays.asList("20", "3"),
                "Subtracts two numbers"
        );
        assertEquals("17", result);
    }

    @Test
    void test_public_ai_function_custom_model() {
        AIResponse dummyResponse = new AIResponse("15");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse, "gpt-3.5-turbo");
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def div(a, b): return a // b",
                Arrays.asList("30", "2"),
                "Divide and floor two numbers",
                "gpt-3.5-turbo"
        );
        assertEquals("15", result);
    }

    @Test
    void test_public_ai_function_no_args() {
        AIResponse dummyResponse = new AIResponse("empty args handled");
        DummyAIClient dummyClient = new DummyAIClient(dummyResponse);
        AIFunctions.aiClient = dummyClient;

        String result = AIFunctions.aiFunction(
                "def hello(): return 'hello'",
                new ArrayList<>(),
                "No-argument greeting function"
        );
        assertEquals("empty args handled", result);
    }

    @Test
    void test_public_ai_function_response_structure() {
        final Map<String, Object>[] capturedParams = new Map[1];
        AIFunctions.aiClient = params -> {
            capturedParams[0] = params;
            return new AIResponse("Y");
        };

        AIFunctions.aiFunction(
                "def echo(s): return s",
                Arrays.asList("foo"),
                "Echo string argument"
        );

        @SuppressWarnings("unchecked")
        List<Map<String, String>> messages = (List<Map<String, String>>) capturedParams[0].get("messages");
        Map<String, String> sysMsg = messages.get(0);
        assertEquals("system", sysMsg.get("role"));
        assertTrue(sysMsg.get("content").toLowerCase().contains("python function"));

        Map<String, String> userMsg = messages.get(1);
        assertEquals("user", userMsg.get("role"));
        assertEquals("foo", userMsg.get("content"));
    }
}