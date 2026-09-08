package com.loong.componentbase.empty_service;

import org.junit.Test;
import static org.junit.Assert.*;

public class EmptyAccountServicePublicTest {
    @Test
    public void testIsLoginDifferent() {
        // Expectation: always false
        EmptyAccountService s = new EmptyAccountService();
        assertFalse(s.isLogin());
    }

    @Test
    public void testGetAccountIdReturnsEmptyStringPublic() {
        EmptyAccountService s = new EmptyAccountService();
        assertEquals("", s.getAccountId());
    }
}