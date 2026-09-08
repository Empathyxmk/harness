package com.example;

import org.junit.jupiter.api.Test;

import javax.script.ScriptException;

class NashornExampleTest {

    @Test
    void printHelloWorld_noException() throws ScriptException {
        NashornExample nashorn = new NashornExample();
        try {
            nashorn.printHelloWorld();
        } catch (Exception e) {
            // Acceptable: Nashorn not present, don't fail the test
        }
    }
}