package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AsyncDaoExceptionPublicTest {

    @Test
    public void testMessage() {
        AsyncDaoException ex = new AsyncDaoException("testPublicMsg");
        assertEquals("testPublicMsg", ex.getMessage());
    }
}