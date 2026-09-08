package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicAuthModeAndExceptionTest {

    @Test
    void testAuthmodeEnum() {
        assertEquals(0, AuthMode.UNAUTHENTICATED.getValue());
        assertEquals(1, AuthMode.WEB.getValue());
        assertEquals(2, AuthMode.APP.getValue());
    }

    @Test
    void testRequiresAuthModeSuccess() {
        class Dummy extends AuthMode.BaseAuthMode {
            Dummy() {
                super(AuthMode.APP);
            }

            @RequiresAuthMode(AuthMode.APP)
            public String foo() {
                return "allowed_public";
            }
        }
        assertEquals("allowed_public", new Dummy().foo());
    }

    @Test
    void testNuExceptionMessage() {
        NuException e = new NuException("public-exception");
        assertEquals("public-exception", e.getMessage());
    }

    @Test
    void testNuInvalidAuthException() {
        String msg = "Bad auth public";
        NuInvalidAuthenticationMethod exc = new NuInvalidAuthenticationMethod(msg);
        assertTrue(exc instanceof NuException);
        assertTrue(exc.getMessage().contains(msg));
    }
}