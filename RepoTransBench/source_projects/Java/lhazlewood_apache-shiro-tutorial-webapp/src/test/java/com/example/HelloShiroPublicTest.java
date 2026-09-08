package com.example;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test class for HelloShiro.
 * Uses different input/output values to test the same functionality.
 */
public class HelloShiroPublicTest {

    HelloShiro shiro;

    @Before
    public void setUp() {
        shiro = new HelloShiro();
    }

    @Test
    public void testLoginSuccess_Public() {
        // Since only "admin"/"adminpass" is valid, test with a similar logic but change string casing to check strict equality
        // Try "Admin"/"Adminpass" (should fail: case sensitive)
        assertFalse(shiro.login("Admin", "Adminpass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        // Now test: use leading/trailing whitespace (should also fail)
        assertFalse(shiro.login(" admin ", " adminpass "));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testLoginFailure_EmptyFields() {
        // Try empty username
        assertFalse(shiro.login("", "adminpass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        // Try empty password
        assertFalse(shiro.login("admin", ""));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testLoginFailure_NullFields() {
        // Try null username (should handle gracefully)
        assertFalse(shiro.login(null, "adminpass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        // Try null password
        assertFalse(shiro.login("admin", null));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testLogoutAfterFailedLogin() {
        assertFalse(shiro.login("nope", "nope"));
        shiro.logout();
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testWelcomeMessage_AdminAfterManualSet() throws Exception {
        // Use reflection to set user = "Admin" (not "admin"), different string
        java.lang.reflect.Field authField = shiro.getClass().getDeclaredField("authenticated");
        authField.setAccessible(true);
        authField.set(shiro, true);
        java.lang.reflect.Field userField = shiro.getClass().getDeclaredField("user");
        userField.setAccessible(true);
        userField.set(shiro, "Admin");
        // Since switch uses "admin", should use default path for "Admin"
        assertEquals("Welcome, Admin!", shiro.getWelcomeMessage());
    }

    @Test
    public void testMultipleLoginLogoutDifferentUsernames() {
        // Fails with username = "root" (not admin)
        assertFalse(shiro.login("root", "supersecret"));
        shiro.logout();
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        // Fails with username = "user"
        assertFalse(shiro.login("user", "userpass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        // Now authenticate and check values
        assertTrue(shiro.login("admin", "adminpass"));
        assertTrue(shiro.isAuthenticated());
        assertEquals("admin", shiro.getUser());
        assertEquals("Welcome, admin!", shiro.getWelcomeMessage());
    }
}