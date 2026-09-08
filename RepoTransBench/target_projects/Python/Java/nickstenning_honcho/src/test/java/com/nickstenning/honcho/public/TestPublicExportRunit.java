package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.RunitExporter;

class TestPublicExportRunit {

    @Test
    void testPublicRunitExporterServiceName() {
        RunitExporter exporter = new RunitExporter();
        String name = exporter.getServiceName("web");
        assertEquals("web", name);
    }
}