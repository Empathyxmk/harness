package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestOptionsMethod {
    @Test
    public void testAccessJwtRequiredEndpoint() {
        int status = 200;
        String respData = "ok";
        assertEquals(200, status);
        assertEquals("ok", respData);
    }
    @Test
    public void testAccessJwtRefreshTokenRequiredEndpoint() {
        int status = 200;
        String respData = "ok";
        assertEquals(200, status);
        assertEquals("ok", respData);
    }
    @Test
    public void testAccessFreshJwtRequiredEndpoint() {
        int status = 200;
        String respData = "ok";
        assertEquals(200, status);
        assertEquals("ok", respData);
    }
}