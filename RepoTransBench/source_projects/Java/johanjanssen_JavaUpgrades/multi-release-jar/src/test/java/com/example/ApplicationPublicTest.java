package com.example;

import org.junit.jupiter.api.Test;

class ApplicationPublicTest {

    @Test
    void main_runsWithoutException_public() {
        // No arguments, should not throw
        Application.main(new String[]{});
    }
}