package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.UpstartExporter;

class TestPublicExportUpstart {

    @Test
    void testPublicUpstartJobName() {
        UpstartExporter exporter = new UpstartExporter();
        String job = exporter.getJobName("scheduler");
        assertEquals("scheduler", job);
    }
}