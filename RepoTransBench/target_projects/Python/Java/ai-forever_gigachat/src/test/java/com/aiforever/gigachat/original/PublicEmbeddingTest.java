package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class Embedding {
    List<Double> values;
    String text;

    public Embedding(List<Double> values, String text) {
        this.values = values;
        this.text = text;
    }
}

public class PublicEmbeddingTest {
    @Test
    void testEmbeddingInit() {
        List<Double> vals = Arrays.asList(0.1, 1.5, 3.1415);
        Embedding e = new Embedding(vals, "hello world");
        assertEquals(vals, e.values);
        assertEquals("hello world", e.text);
    }

    @Test
    void testEmbeddingValuesSize() {
        Embedding e = new Embedding(Arrays.asList(1.0, 2.0, 3.0), "test");
        assertEquals(3, e.values.size());
        assertEquals(Double.valueOf(1.0), e.values.get(0));
    }
}