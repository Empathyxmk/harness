package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.SystemdExporter;

class TestPublicExportSystemd {

    @Test
    void testPublicSystemdUnitName() {
        SystemdExporter exporter = new SystemdExporter();
        String unit = exporter.getUnitName("api");
        assertEquals("api.service", unit);
    }
}