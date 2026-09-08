package com.nateshmbhat.pyttsx3.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class AnotherDummyEngineApi {
    String driverName;
    public AnotherDummyEngineApi(String driverName, boolean debug) { this.driverName = driverName; }
    public String say(String text) { return new StringBuilder(text).reverse().toString(); }
    public String runAndWait() { return "executed"; }
    public String stop() { return "halted"; }
    public Object get(String name) { return "default"; }
}

class PublicPyttsx3Api {
    static Map<String, AnotherDummyEngineApi> _activeEngines = new HashMap<>();
    public static AnotherDummyEngineApi init(String driverName) {
        return init(driverName, false);
    }
    public static AnotherDummyEngineApi init(String driverName, boolean debug) {
        if (_activeEngines.containsKey(driverName)) {
            return _activeEngines.get(driverName);
        }
        AnotherDummyEngineApi eng = new AnotherDummyEngineApi(driverName, debug);
        _activeEngines.put(driverName, eng);
        return eng;
    }
}

public class PublicPyttsx3ApiTest {
    @BeforeEach
    void clearEngines() { PublicPyttsx3Api._activeEngines.clear(); }

    @Test
    void testPublicInitAndEngine() {
        AnotherDummyEngineApi engine = PublicPyttsx3Api.init("diffdummy");
        assertEquals("diffdummy", engine.driverName);
    }

    @Test
    void testPublicEngineCache() {
        AnotherDummyEngineApi e1 = PublicPyttsx3Api.init("cachetestA");
        AnotherDummyEngineApi e2 = PublicPyttsx3Api.init("cachetestA");
        assertSame(e1, e2);
    }

    @Test
    void testPublicEngineUnique() {
        AnotherDummyEngineApi e1 = PublicPyttsx3Api.init("uniqueA");
        AnotherDummyEngineApi e2 = PublicPyttsx3Api.init("uniqueB");
        assertNotSame(e1, e2);
    }

    @Test
    void testPublicEngineMethods() {
        AnotherDummyEngineApi e = PublicPyttsx3Api.init("diffdummy");
        assertEquals("rab", e.say("bar"));
        assertEquals("executed", e.runAndWait());
        assertEquals("halted", e.stop());
    }
}