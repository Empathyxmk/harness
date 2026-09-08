package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AJPFuzzerExtraPublicTest {

    @Test
    void testMainHandlesArgs() {
        AJPFuzzer.main(new String[]{"test", "case"});
    }
}