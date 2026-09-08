package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExceptionsTest {
    
    @Test
    void testCypherSyntaxErrorException() {
        CypherSyntaxErrorException ex = new CypherSyntaxErrorException("msg");
        assertEquals("msg", ex.getMessage());
    }

    @Test
    void testVersionMismatchException() {
        VersionMismatchException ex = new VersionMismatchException("mismatch!");
        assertEquals("mismatch!", ex.getMessage());
    }

    @Test
    void testQueryEmptyException() {
        QueryEmptyException ex = new QueryEmptyException();
        assertTrue(ex instanceof QueryEmptyException);
    }
}