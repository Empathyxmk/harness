package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicPTqdmVersion {
    public static final String __version__ = "1.4.2";
}
public class TestPublicVersion {
    @Test
    void testVersion() {
        assertTrue(PublicPTqdmVersion.__version__ instanceof String);
        assertTrue(PublicPTqdmVersion.__version__.matches("\\d+\\.\\d+\\.\\d+"));
    }
}