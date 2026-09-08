package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

class AJPFuzzerExtraTest {

    @Test
    void testMainRunsAndDoesNotFail() {
        // The main does nothing but can be invoked for coverage
        AJPFuzzer.main(new String[] {});
    }
}