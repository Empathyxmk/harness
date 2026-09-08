package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AsyncDaoExceptionTest {

    @Test
    public void testMessage() {
        AsyncDaoException ex = new AsyncDaoException("msg");
        assertEquals("msg", ex.getMessage());
    }
}