package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.BaseExporter;

class TestExportBase {

    @Test
    void testExporterHasTemplateDir() {
        BaseExporter exporter = new BaseExporter();
        assertNotNull(exporter.getTemplateDir());
    }
}