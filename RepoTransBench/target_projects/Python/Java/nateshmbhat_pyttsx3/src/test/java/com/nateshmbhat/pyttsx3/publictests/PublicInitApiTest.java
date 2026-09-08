package com.nateshmbhat.pyttsx3.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class YetAnotherDummyEngineApi {
    String name;
    public YetAnotherDummyEngineApi(String driverName, boolean debug) { this.name = driverName; }
    public String start() { return "hello"; }
    public String finish() { return "goodbye"; }
}

class PublicPyttsx3InitApi {
    static Map<String, YetAnotherDummyEngineApi> _activeEngines = new HashMap<>();
    public static YetAnotherDummyEngineApi init(String driverName) {
        return init(driverName, false);
    }
    public static YetAnotherDummyEngineApi init(String driverName, boolean debug) {
        if (_activeEngines.containsKey(driverName)) {
            return _activeEngines.get(driverName);
        }
        YetAnotherDummyEngineApi eng = new YetAnotherDummyEngineApi(driverName, debug);
        _activeEngines.put(driverName, eng);
        return eng;
    }
}

public class PublicInitApiTest {
    @BeforeEach
    void clearEngines() { PublicPyttsx3InitApi._activeEngines.clear(); }

    @Test
    void testPublicEngineCreation() {
        YetAnotherDummyEngineApi engine = PublicPyttsx3InitApi.init("publicengine");
        assertEquals("publicengine", engine.name);
    }

    @Test
    void testPublicEngineSingleton() {
        YetAnotherDummyEngineApi e1 = PublicPyttsx3InitApi.init("publicdummyA");
        YetAnotherDummyEngineApi e2 = PublicPyttsx3InitApi.init("publicdummyA");
        assertSame(e1, e2);
    }

    @Test
    void testPublicEngineDifferent() {
        YetAnotherDummyEngineApi e1 = PublicPyttsx3InitApi.init("public1");
        YetAnotherDummyEngineApi e2 = PublicPyttsx3InitApi.init("public2");
        assertNotSame(e1, e2);
    }
}