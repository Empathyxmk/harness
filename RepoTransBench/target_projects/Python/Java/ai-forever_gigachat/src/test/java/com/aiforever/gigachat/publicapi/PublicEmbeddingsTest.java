package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class Embedding {
    List<Double> vals;

    Embedding(List<Double> vals) {
        this.vals = vals;
    }
}

public class PublicEmbeddingsTest {
    @Test
    void testBasicEmbedding() {
        Embedding e = new Embedding(Arrays.asList(0.0, 1.0, 2.0));
        assertEquals(3, e.vals.size());
        assertEquals(0.0, e.vals.get(0));
        assertEquals(2.0, e.vals.get(2));
    }

    @Test
    void testComplexVectorEmbedding() {
        Embedding e = new Embedding(Arrays.asList(1.0, 1.5, 2.5, 3.5));
        assertTrue(e.vals.stream().allMatch(v -> v >= 1.0));
        assertEquals(4, e.vals.size());
    }
}