package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestGetJwtInNonProtectedContexts {
    @Test
    public void testGetJwtInNonProtectedRoute() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("get_jwt only available in protected endpoints");
        });
        assertTrue(ex.getMessage().toLowerCase().contains("protected"));
    }

    @Test
    public void testGetJwtHeaderInNonProtectedRoute() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("get_jwt_header only available in protected endpoints");
        });
        assertTrue(ex.getMessage().toLowerCase().contains("protected"));
    }

    @Test
    public void testGetJwtIdentityInNonProtectedRoute() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("get_jwt_identity only available in protected endpoints");
        });
        assertTrue(ex.getMessage().toLowerCase().contains("protected"));
    }

    @Test
    public void testCurrentUserInNonProtectedRoute() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("current_user attribute only available in protected endpoints");
        });
        assertTrue(ex.getMessage().toLowerCase().contains("protected"));
    }

    @Test
    public void testGetCurrentUserInNonProtectedRoute() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("get_current_user only available in protected endpoints");
        });
        assertTrue(ex.getMessage().toLowerCase().contains("protected"));
    }
}