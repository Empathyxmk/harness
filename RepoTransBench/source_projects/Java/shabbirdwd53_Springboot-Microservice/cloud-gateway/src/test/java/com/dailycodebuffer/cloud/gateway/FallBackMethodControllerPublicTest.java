package com.dailycodebuffer.cloud.gateway;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FallBackMethodControllerPublicTest {
    @Test
    void testDepartmentServiceFallBackWithAnotherParam() {
        FallBackMethodController controller = new FallBackMethodController();
        String input = "publicExample";
        String result = controller.departmentServiceFallBack(input);
        // Ensure the fallback message is part of the result, and the chosen input is included
        assertTrue(result.contains("Department Service is taking longer"));
        assertTrue(result.contains(input));
    }

    @Test
    void testDepartmentServiceFallBack_EmptyStringParam() {
        FallBackMethodController controller = new FallBackMethodController();
        String result = controller.departmentServiceFallBack("");
        assertTrue(result.contains("Department Service is taking longer"));
        // It should also work with an empty string as parameter and return the fallback message
    }
}