package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InitTest {
    @Test
    public void testInitRuns() {
        try {
            Class<?> pyicloudCls = Class.forName("com.picklepete.pyicloud.PyiCloudService");
            assertNotNull(pyicloudCls);
            assertNotNull(pyicloudCls.getPackage());
            assertEquals("PyiCloudService", pyicloudCls.getSimpleName());
        } catch (ClassNotFoundException e) {
            fail("PyiCloudService class not found");
        }
    }
}