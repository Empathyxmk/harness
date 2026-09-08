package com.example;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class HelloShiroTest {

    HelloShiro shiro;

    @Before
    public void setUp() {
        shiro = new HelloShiro();
    }

    @Test
    public void testLoginSuccess() {
        assertTrue(shiro.login("admin", "adminpass"));
        assertTrue(shiro.isAuthenticated());
        assertEquals("admin", shiro.getUser());
        assertEquals("Welcome, admin!", shiro.getWelcomeMessage());
    }

    @Test
    public void testLoginFailure_BadPassword() {
        assertFalse(shiro.login("admin", "wrongpass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testLoginFailure_UnknownUser() {
        assertFalse(shiro.login("bob", "somepass"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testLogout() {
        shiro.login("admin", "adminpass");
        shiro.logout();
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testWelcomeMessageNotAuthenticated() {
        assertEquals("Please log in.", shiro.getWelcomeMessage());
    }

    @Test
    public void testWelcomeMessageUnknownUser() throws Exception {
        // Use reflection to set user to something else, as only "admin" passes login
        java.lang.reflect.Field authField = shiro.getClass().getDeclaredField("authenticated");
        authField.setAccessible(true);
        authField.set(shiro, true);
        java.lang.reflect.Field userField = shiro.getClass().getDeclaredField("user");
        userField.setAccessible(true);
        userField.set(shiro, "otheruser");
        assertEquals("Welcome, otheruser!", shiro.getWelcomeMessage());
    }

    @Test
    public void testMultipleLoginLogoutCycles() {
        assertTrue(shiro.login("admin", "adminpass"));
        shiro.logout();
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        assertFalse(shiro.login("test", "bad"));
        assertFalse(shiro.isAuthenticated());
        assertNull(shiro.getUser());
        assertEquals("Please log in.", shiro.getWelcomeMessage());

        assertTrue(shiro.login("admin", "adminpass"));
        assertTrue(shiro.isAuthenticated());
        assertEquals("admin", shiro.getUser());
    }
}