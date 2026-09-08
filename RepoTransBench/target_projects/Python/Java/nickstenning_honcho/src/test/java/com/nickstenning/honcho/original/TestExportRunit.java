package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.RunitExporter;

class TestExportRunit {

    @Test
    void testRunitExporterServiceName() {
        RunitExporter exporter = new RunitExporter();
        String name = exporter.getServiceName("web");
        assertEquals("web", name);
    }
}