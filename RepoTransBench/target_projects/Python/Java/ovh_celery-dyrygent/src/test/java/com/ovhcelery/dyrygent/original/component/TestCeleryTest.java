package com.ovhcelery.dyrygent.original.component;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.ovhcelery.dyrygent.celery.inspect;

import java.util.*;

class TestCeleryInspect {

    @Test
    void testChainTasks() {
        // Assuming chain operations: signature list, chain, inspect
        List<Object> sigs = new ArrayList<>();
        for (int i = 0; i < 4; i++) sigs.add(new Signature());
        Object chain = chain(sigs); // simulate
        List<Object> tasks = inspect.getChainTasks(chain);
        assertEquals(sigs, tasks);
    }

    @Test
    void testChordTasks() {
        List<Object> sigs = new ArrayList<>();
        for (int i = 0; i < 4; i++) sigs.add(new Signature());
        Object barrier = new Signature();
        Object chord = chord(sigs, barrier);
        Object[] result = inspect.getChordTasks(chord);
        List<Object> tasks = (List<Object>) result[1];
        Object body = result[0];
        assertEquals(sigs, tasks);
        assertEquals(barrier, body);
    }

    @Test
    void testGroupTasks() {
        List<Object> sigs = Arrays.asList(new Signature(), new Signature(), new Signature(), new Signature());
        Object group = group(sigs); // simulate
        List<Object> tasks = inspect.getGroupTasks(group);
        assertEquals(sigs, tasks);
    }

    @Test
    void testSignatureFreeze() {
        Signature sig = new Signature();
        sig.freeze();
        assertNotNull(sig.id());
    }
}