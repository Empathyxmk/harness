package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.UUID;

public class TestUuid {

    @Test
    public void testGeneratedUuid() {
        UUID uuid = UUID.randomUUID();
        assertNotNull(uuid, "UUID was not generated.");
    }
}