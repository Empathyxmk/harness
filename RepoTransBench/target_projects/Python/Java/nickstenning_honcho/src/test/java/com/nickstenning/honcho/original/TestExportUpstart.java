package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.UpstartExporter;

class TestExportUpstart {

    @Test
    void testUpstartJobName() {
        UpstartExporter exporter = new UpstartExporter();
        String job = exporter.getJobName("scheduler");
        assertEquals("scheduler", job);
    }
}