package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDispatcher {
    @Test
    void testBasicDispatch() {
        EventDispatcher dispatcher = new EventDispatcher();
        dispatcher.registerHandler("my-event", event -> "foo event handled");
        String result = dispatcher.dispatch("my-event");
        assertEquals("foo event handled", result);
    }

    @Test
    void testDispatchNoRegisteredHandler() {
        EventDispatcher dispatcher = new EventDispatcher();
        Exception ex = assertThrows(IllegalArgumentException.class, () -> dispatcher.dispatch("random-evt"));
        assertEquals("No handler for event: random-evt", ex.getMessage());
    }

    @Test
    void testMultipleEventHandlers() {
        EventDispatcher dispatcher = new EventDispatcher();
        dispatcher.registerHandler("evt1", event -> "one");
        dispatcher.registerHandler("evt2", event -> "two");

        assertEquals("one", dispatcher.dispatch("evt1"));
        assertEquals("two", dispatcher.dispatch("evt2"));
    }

    // Minimalistic dispatcher simulation for test context
    private static class EventDispatcher {
        private final java.util.Map<String, java.util.function.Function<String, String>> handlers = new java.util.HashMap<>();
        void registerHandler(String evt, java.util.function.Function<String, String> fn) {
            handlers.put(evt, fn);
        }
        String dispatch(String evt) {
            java.util.function.Function<String, String> fn = handlers.get(evt);
            if (fn == null)
                throw new IllegalArgumentException("No handler for event: " + evt);
            return fn.apply(evt);
        }
    }
}