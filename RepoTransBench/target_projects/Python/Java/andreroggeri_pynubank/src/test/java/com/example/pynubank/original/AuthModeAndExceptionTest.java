package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AuthModeAndExceptionTest {

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
                super(AuthMode.WEB);
            }

            @RequiresAuthMode(AuthMode.WEB)
            public String foo() {
                return "allowed";
            }
        }
        assertEquals("allowed", new Dummy().foo());
    }

    @Test
    void testRequiresAuthModeFailure() {
        class Dummy extends AuthMode.BaseAuthMode {
            Dummy() {
                super(AuthMode.UNAUTHENTICATED);
            }

            @RequiresAuthMode(AuthMode.WEB)
            public String foo() {
                return "denied";
            }
        }

        Dummy d = new Dummy();
        assertThrows(NuInvalidAuthenticationMethod.class, d::foo);
    }

    @Test
    void testNuExceptionMessage() {
        NuException e = new NuException("hello");
        assertEquals("hello", e.getMessage());
    }

    @Test
    void testNuInvalidAuthException() {
        String msg = "Bad auth";
        NuInvalidAuthenticationMethod exc = new NuInvalidAuthenticationMethod(msg);
        assertTrue(exc instanceof NuException);
        assertTrue(exc.getMessage().contains(msg));
    }

    @Test
    void testNuMissingCreditCardException() {
        NuMissingCreditCard e = new NuMissingCreditCard();
        assertTrue(e.getMessage().toLowerCase().contains("missing credit card"));
    }

    private static DummyResponse fakeResponse() {
        return new DummyResponse(404, "http://test");
    }

    @Test
    void testRequestException() {
        DummyResponse r = fakeResponse();
        NuRequestException exc = new NuRequestException(r);
        assertEquals(404, exc.getStatusCode());
        assertEquals("http://test", exc.getUrl());
        assertTrue(exc.getMessage().startsWith("The request made failed with HTTP status code"));
    }
}