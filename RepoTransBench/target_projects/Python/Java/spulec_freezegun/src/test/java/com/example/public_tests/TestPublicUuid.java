package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.UUID;

public class TestPublicUuid {

    @Test
    public void testUuidNotNull() {
        assertNotNull(UUID.randomUUID());
    }
}