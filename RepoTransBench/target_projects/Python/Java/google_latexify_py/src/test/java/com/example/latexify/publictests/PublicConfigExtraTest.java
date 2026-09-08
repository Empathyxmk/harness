package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicConfigExtraTest {

    static class Cfg {
        boolean enabled = true;
        void disable() { enabled = false; }
        boolean isEnabled() { return enabled; }
    }

    @Test
    void testDisable() {
        Cfg cfg = new Cfg();
        cfg.disable();
        assertFalse(cfg.isEnabled());
    }
}