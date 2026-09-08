package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class Example {
    String input, output;

    public Example(String input, String output) {
        this.input = input;
        this.output = output;
    }
}

class ComplexExample {
    Map<String, Object> args;
    String result;

    public ComplexExample(Map<String, Object> args, String result) {
        this.args = args;
        this.result = result;
    }
}

public class ExamplesTest {
    @Test
    void testExampleCreation() {
        Example e = new Example("big data", "Big Data!");
        assertEquals("big data", e.input);
        assertEquals("Big Data!", e.output);
    }

    @Test
    void testComplexExample() {
        Map<String, Object> args = new HashMap<>();
        args.put("num", 7);
        args.put("msg", "hi");
        ComplexExample ce = new ComplexExample(args, "ok");
        assertEquals(2, ce.args.size());
        assertEquals(7, ce.args.get("num"));
        assertEquals("ok", ce.result);
    }
}