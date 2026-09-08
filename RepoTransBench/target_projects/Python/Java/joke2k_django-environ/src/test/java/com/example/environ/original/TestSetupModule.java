package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestSetupModule {

    @Test
    void testSetupWorks() {
        // Setup code runs, module code is loaded, etc.
        // This usually checks for side-effects, just ensure classes exist
        assertNotNull(new Env());
        assertNotNull(new FileAwareMapping());
    }
}