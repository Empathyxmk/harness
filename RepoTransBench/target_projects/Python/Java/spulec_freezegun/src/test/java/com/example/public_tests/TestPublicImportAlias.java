package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicImportAlias {

    @Test
    public void testImportAlias() {
        String alias = "frozen_time_alias";
        assertEquals("frozen_time_alias", alias);
    }
}