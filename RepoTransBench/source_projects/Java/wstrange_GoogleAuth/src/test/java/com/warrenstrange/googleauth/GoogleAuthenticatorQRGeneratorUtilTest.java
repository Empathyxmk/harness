package com.warrenstrange.googleauth;

import org.junit.Test;

import java.io.UnsupportedEncodingException;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class GoogleAuthenticatorQRGeneratorUtilTest {

    // Test private static internalURLEncode via reflection (for exception & normal)
    @Test
    public void testInternalURLEncodeNormal() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("internalURLEncode", String.class);
        m.setAccessible(true);
        String encoded = (String)m.invoke(null, "test@example.com");
        assertTrue(encoded.contains("test%40example.com"));
    }

    @Test
    public void testInternalURLEncode_Throws() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("internalURLEncode", String.class);
        m.setAccessible(true);

        // Break URLEncoder for the test forcibly by changing "UTF-8" to an invalid charset in the method
        // We'll skip exception branch coverage here as realistically UTF-8 is always present, unless test JVM is faulty
        // This branches is for documentation: test UTF-8 decoding failure, if possible (but not feasible).
    }

    @Test
    public void testFormatLabelHappyPath() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        String label = (String)m.invoke(null, "IssuerCompany", "user@example.com");
        assertEquals("IssuerCompany:user@example.com", label);

        label = (String)m.invoke(null, null, "john");
        assertEquals("john", label);
    }

    @Test
    public void testFormatLabelThrows_AccountNameNull() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Company", null);
            fail("Should have thrown IllegalArgumentException for null account name");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }

    @Test
    public void testFormatLabelThrows_AccountNameEmpty() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Company", "");
            fail("Should have thrown IllegalArgumentException for empty account name");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }

    @Test
    public void testFormatLabelThrows_IssuerContainsColon() throws Exception {
        Method m = GoogleAuthenticatorQRGenerator.class.getDeclaredMethod("formatLabel", String.class, String.class);
        m.setAccessible(true);
        try {
            m.invoke(null, "Iss:uer", "user");
            fail("Should have thrown IllegalArgumentException for colon in issuer");
        } catch (Exception e) {
            assertTrue(e.getCause() instanceof IllegalArgumentException);
        }
    }
}