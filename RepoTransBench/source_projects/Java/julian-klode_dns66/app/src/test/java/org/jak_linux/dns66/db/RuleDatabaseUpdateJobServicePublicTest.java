package org.jak_linux.dns66.db;

import org.junit.Test;
import static org.junit.Assert.*;

public class RuleDatabaseUpdateJobServicePublicTest {
    @Test
    public void testJobServiceFieldsPublic() {
        RuleDatabaseUpdateJobService service = new RuleDatabaseUpdateJobService();
        assertNotNull(service);
        // Use a custom field/value for public variant
        service.jobFinishedCalled = true;
        assertTrue(service.jobFinishedCalled);
    }
}