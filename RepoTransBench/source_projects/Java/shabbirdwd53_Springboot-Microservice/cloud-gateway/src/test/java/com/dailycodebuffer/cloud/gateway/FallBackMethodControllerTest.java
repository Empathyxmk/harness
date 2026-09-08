package com.dailycodebuffer.cloud.gateway;

import com.dailycodebuffer.cloud.gateway.FallBackMethodController;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FallBackMethodControllerTest {
    @Test
    void testDepartmentServiceFallBack() {
        FallBackMethodController controller = new FallBackMethodController();
        String result = controller.departmentServiceFallBack("test");
        assertTrue(result.contains("Department Service is taking longer"));
        assertTrue(result.contains("test"));
    }

    @Test
    void testDepartmentServiceFallBack_NullParam() {
        FallBackMethodController controller = new FallBackMethodController();
        String result = controller.departmentServiceFallBack(null);
        assertTrue(result.contains("Department Service is taking longer"));
    }
}