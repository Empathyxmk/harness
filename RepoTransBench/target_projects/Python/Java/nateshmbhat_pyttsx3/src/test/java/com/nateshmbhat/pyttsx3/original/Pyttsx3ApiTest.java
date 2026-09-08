package com.nateshmbhat.pyttsx3.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class DummyEngineApi {
    String driverName;
    public DummyEngineApi() {}
    public DummyEngineApi(String driverName, boolean debug) {
        this.driverName = driverName;
    }
    public String say(String text) {
        return text;
    }
    public String runAndWait() {
        return "ran";
    }
    public String stop() {
        return "stopped";
    }
}

class Pyttsx3Api {
    static Map<String, DummyEngineApi> _activeEngines = new HashMap<>();
    public static DummyEngineApi init(String driverName) { return init(driverName, false); }
    public static DummyEngineApi init(String driverName, boolean debug) {
        if (_activeEngines.containsKey(driverName))
            return _activeEngines.get(driverName);
        DummyEngineApi eng = new DummyEngineApi(driverName, debug);
        _activeEngines.put(driverName, eng);
        return eng;
    }
}

public class Pyttsx3ApiTest {

    @BeforeEach
    void clearEngines() {
        Pyttsx3Api._activeEngines.clear();
    }

    @Test
    void testInitAndEngine() {
        DummyEngineApi engine = Pyttsx3Api.init("dummy");
        assertEquals("dummy", engine.driverName);
    }

    @Test
    void testEngineCache() {
        DummyEngineApi e1 = Pyttsx3Api.init("dummy");
        DummyEngineApi e2 = Pyttsx3Api.init("dummy");
        assertSame(e1, e2);
    }

    @Test
    void testEngineUnique() {
        DummyEngineApi e1 = Pyttsx3Api.init("dummy1");
        DummyEngineApi e2 = Pyttsx3Api.init("dummy2");
        assertNotSame(e1, e2);
    }

    @Test
    void testEngineMethods() {
        DummyEngineApi e = Pyttsx3Api.init("dummy");
        assertEquals("foo", e.say("foo"));
        assertEquals("ran", e.runAndWait());
        assertEquals("stopped", e.stop());
    }
}