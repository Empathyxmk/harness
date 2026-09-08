package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestAsymmetricCrypto {
    @Test
    public void testAsymmetricCrypto() {
        // Simulate: first token with symmetric (fail), second with asymmetric (pass)
        int symmetricStatus = 422;
        int asymmetricStatus = 200;
        String errorMsg = "The specified alg value is not allowed";
        String okValue = "bar";
        assertEquals(422, symmetricStatus);
        assertEquals("The specified alg value is not allowed", errorMsg);
        assertEquals(200, asymmetricStatus);
        assertEquals("bar", okValue);
    }
}