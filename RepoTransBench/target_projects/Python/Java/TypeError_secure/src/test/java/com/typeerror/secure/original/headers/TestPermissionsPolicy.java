package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.PermissionsPolicy;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPermissionsPolicy {

    @Test
    public void testDefaultPermissionsPolicy() {
        PermissionsPolicy policy = new PermissionsPolicy();
        assertEquals("geolocation=(), microphone=(), camera=()", policy.getHeaderValue());
    }

    @Test
    public void testCustomPermissionsPolicy() {
        PermissionsPolicy policy = new PermissionsPolicy().camera("'self'").geolocation("'none'");
        assertEquals("camera=('self'), geolocation=('none')", policy.getHeaderValue());
    }

    @Test
    public void testClearPermissionsPolicy() {
        PermissionsPolicy policy = new PermissionsPolicy().camera("'self'").clear();
        assertEquals("geolocation=(), microphone=(), camera=()", policy.getHeaderValue());
    }

    @Test
    public void testAddDirective() {
        PermissionsPolicy policy = new PermissionsPolicy().addDirective("microphone", "'self'");
        assertTrue(policy.getHeaderValue().contains("microphone=('self')"));
    }
}