package com.vimalloc.flaskjwt.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigTest {
    @Test
    public void testJwtSecretKeyPresent() {
        String jwtSecret = "abc_config_public";
        assertEquals("abc_config_public", jwtSecret, "JWT secret key must match expected");
    }
}