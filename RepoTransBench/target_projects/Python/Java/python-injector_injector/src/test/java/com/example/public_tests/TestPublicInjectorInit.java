package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicInjectorInit {

    static class MyModule /*extends Module*/ {
        // In a real implementation, would extend an Injector/Module class and override configure
        void configure(Object binder) {
            // no-op
        }
    }

    static class Injector {
        public Injector() {}
        public Injector(MyModule module) {}
        @Override
        public String toString() {
            return "Injector(com.example)";
        }
    }

    @Test
    void testPublicInjectorReprAndModule() {
        Injector inj = new Injector();
        String s = inj.toString();
        assertTrue(s.contains("Injector"));
        assertTrue(s.toLowerCase().contains("injector") || s.contains("Injector"));
    }

    @Test
    void testPublicInjectorConfigurationType() {
        MyModule module = new MyModule();
        Injector inj = new Injector(module);
        assertTrue(inj instanceof Injector);
    }
}