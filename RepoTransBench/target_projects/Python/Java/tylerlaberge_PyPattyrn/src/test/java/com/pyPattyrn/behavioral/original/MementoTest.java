package com.pyPattyrn.behavioral.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import com.pyPattyrn.behavioral.memento.Memento;
import com.pyPattyrn.behavioral.memento.Originator;

class MementoTest {
    private Map<String, String> state;

    @BeforeEach
    void setUp() {
        state = new HashMap<>();
        state.put("foo", "bar");
    }

    @Test
    void testInit() {
        Memento memento = new Memento(state);
        assertEquals("bar", memento.getState().get("foo"));
    }

    @Test
    void testOriginatorSaveRestore() {
        Originator<Map<String, String>> originator = new Originator<>();
        originator.setState(state);
        Memento memento = originator.save();
        state.put("foo", "baz");
        originator.restore(memento);
        assertEquals("bar", originator.getState().get("foo"));
    }
}