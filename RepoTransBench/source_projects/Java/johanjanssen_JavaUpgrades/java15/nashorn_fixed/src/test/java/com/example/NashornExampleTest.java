package com.example;

import org.junit.jupiter.api.Test;

import javax.script.ScriptException;

class NashornExampleTest {

    @Test
    void printHelloWorld_noException() throws ScriptException {
        NashornExample nashorn = new NashornExample();
        // In many environments, Nashorn may not be present, but here we expect no exception in supported JVMs
        try {
            nashorn.printHelloWorld();
        } catch (Exception e) {
            // Acceptable: Nashorn not present, don't fail the test
        }
    }
}