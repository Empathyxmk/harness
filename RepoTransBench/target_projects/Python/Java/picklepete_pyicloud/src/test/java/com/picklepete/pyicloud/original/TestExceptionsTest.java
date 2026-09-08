package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestExceptionsTest {
    @Test
    public void testRaiseICloudException() {
        Exception e = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("ICloudException: Something went wrong!");
        });
        assertEquals("ICloudException: Something went wrong!", e.getMessage());
    }

    @Test
    public void testTwoStepAuthException() {
        Exception e = assertThrows(IllegalStateException.class, () -> {
            throw new IllegalStateException("Two-step authentication required");
        });
        assertEquals("Two-step authentication required", e.getMessage());
    }
}