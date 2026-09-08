package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Environ;

class TestPublicEnviron {

    @Test
    void testPublicEnvironRead() {
        Environ env = new Environ();
        env.put("FOO", "BAR");
        assertEquals("BAR", env.get("FOO"));
    }
}