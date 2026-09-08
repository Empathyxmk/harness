package com.warrenstrange.googleauth;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class GoogleAuthenticatorQRGeneratorUtilPublicTest {

    @Test
    public void testInternalURLEncodeNormal_public() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("internalURLEncode", String.class);
        m.setAccessible(true);
        String encoded = (String)m.invoke(null, "hello+world@example.org");
        assertTrue(encoded.contains("hello%2Bworld%40example.org"));
    }

    // No need to re-implement exception branch, as in original (realistically unreachable branch unless JVM is broken).

    @Test
    public void testFormatLabelHappyPath_public() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        String label = (String)m.invoke(null, "OtherIssuer", "publicuser@domain.net");
        assertEquals("OtherIssuer:publicuser@domain.net", label);

        label = (String)m.invoke(null, null, "bob");
        assertEquals("bob", label);
    }

    @Test
    public void testFormatLabelThrows_AccountNameNull_public() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Acme", null);
            fail("Should have thrown IllegalArgumentException for null account name");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }

    @Test
    public void testFormatLabelThrows_AccountNameEmpty_public() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Acme", "");
            fail("Should have thrown IllegalArgumentException for empty account name");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }

    @Test
    public void testFormatLabelThrows_IssuerContainsColon_public() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Not:Valid", "janedoe");
            fail("Should have thrown IllegalArgumentException for colon in issuer");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }
}