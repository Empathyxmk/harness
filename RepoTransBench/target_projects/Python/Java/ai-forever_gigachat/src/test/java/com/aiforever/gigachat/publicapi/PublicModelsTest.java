package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ModelInfo {
    String name;
    String version;
    ModelInfo(String name, String version) {
        this.name = name;
        this.version = version;
    }
}

public class PublicModelsTest {
    @Test
    void testModelName() {
        ModelInfo m = new ModelInfo("gigachat", "1.0");
        assertEquals("gigachat", m.name);
        assertEquals("1.0", m.version);
    }

    @Test
    void testModelDifferentVersion() {
        ModelInfo m = new ModelInfo("gigachat", "2.0");
        assertEquals("2.0", m.version);
        assertNotEquals("1.0", m.version);
    }
}