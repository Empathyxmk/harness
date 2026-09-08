package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PTqdmVersion {
    public static final String __version__ = "1.4.2";
}

public class TestVersion {
    @Test
    void testVersion() {
        assertTrue(PTqdmVersion.class.getDeclaredFields().length > 0);
        assertEquals("1.4.2", PTqdmVersion.__version__);
    }
}