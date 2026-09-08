package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.SystemdExporter;

class TestExportSystemd {

    @Test
    void testSystemdUnitName() {
        SystemdExporter exporter = new SystemdExporter();
        String unit = exporter.getUnitName("api");
        assertEquals("api.service", unit);
    }
}