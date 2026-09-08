package com.nateshmbhat.pyttsx3.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class DummyEngineInit {
    public DummyEngineInit(String driverName, boolean debug) {}
    public String say(String text) { return text; }
    public String runAndWait() { return "ran"; }
    public String stop() { return "stopped"; }
}

class Pyttsx3InitApi {
    static Map<String, DummyEngineInit> _activeEngines = new HashMap<>();
    public static DummyEngineInit init(String driverName) {
        return init(driverName, false);
    }
    public static DummyEngineInit init(String driverName, boolean debug) {
        if (_activeEngines.containsKey(driverName))
            return _activeEngines.get(driverName);
        DummyEngineInit eng = new DummyEngineInit(driverName, debug);
        _activeEngines.put(driverName, eng);
        return eng;
    }
    public static void speak(String text) {
        DummyEngineInit engine = Pyttsx3InitApi.init("dummy");
        engine.say(text);
        engine.runAndWait();
    }
}

public class InitApiTest {

    @BeforeEach
    void clearEngines() {
        Pyttsx3InitApi._activeEngines.clear();
    }

    @Test
    void testInitReturnsEngine() {
        DummyEngineInit engine = Pyttsx3InitApi.init("dummy");
        assertNotNull(engine.say("something"));
        assertNotNull(engine.runAndWait());
        assertNotNull(engine.stop());
    }

    @Test
    void testInitReturnsCachedInstance() {
        DummyEngineInit eng1 = Pyttsx3InitApi.init("dummy");
        DummyEngineInit eng2 = Pyttsx3InitApi.init("dummy");
        assertSame(eng1, eng2);
    }

    @Test
    void testInitWithDebugFlag() {
        DummyEngineInit eng = Pyttsx3InitApi.init("dummy", true);
        assertNotNull(eng.say("x"));
    }

    @Test
    void testSpeakCallsInitAndEngineMethods() {
        Map<String, Object> calls = new HashMap<>();
        class DummyEngineLocal extends DummyEngineInit {
            DummyEngineLocal() { super("dummy", false); calls.put("init", true); }
            @Override public String say(String text) { calls.put("say", text); return null; }
            @Override public String runAndWait() { calls.put("run", true); return null; }
        }
        Pyttsx3InitApi._activeEngines.clear();
        Pyttsx3InitApi._activeEngines.put("dummy", new DummyEngineLocal());
        Pyttsx3InitApi.speak("text");
        assertEquals(true, calls.get("init"));
        assertEquals("text", calls.get("say"));
        assertEquals(true, calls.get("run"));
    }
}