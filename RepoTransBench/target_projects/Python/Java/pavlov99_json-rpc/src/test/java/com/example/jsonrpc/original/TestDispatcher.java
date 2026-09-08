package com.example.jsonrpc.original;

import com.example.jsonrpc.dispatcher.MyDispatcher;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestDispatcher {

    private MyDispatcher dispatcher;

    @BeforeEach
    void setUp() {
        dispatcher = new MyDispatcher();
        dispatcher.register("add", (params) -> {
            int sum = 0;
            for (Object o : params) {
                sum += Integer.valueOf(o.toString());
            }
            return sum;
        });
    }

    @Test
    void testRegisteredMethodWorks() {
        Object res = dispatcher.dispatch("add", new Object[] {1, 2, 3});
        assertEquals(6, res);
    }

    @Test
    void testUnregisteredMethodThrows() {
        assertThrows(IllegalArgumentException.class, () ->
                dispatcher.dispatch("subtract", new Object[] {1,2}));
    }
}