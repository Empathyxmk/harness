package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AJPFuzzerPublicTest {

    @Test
    void testMainNoCrash() {
        AJPFuzzer.main(new String[]{"--version"});
        AJPFuzzer.main(new String[0]);
    }
}