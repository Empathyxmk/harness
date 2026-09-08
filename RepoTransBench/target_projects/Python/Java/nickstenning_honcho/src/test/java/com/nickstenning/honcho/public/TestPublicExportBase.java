package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.BaseExporter;

class TestPublicExportBase {

    @Test
    void testPublicBaseExporterTemplateDirExists() {
        BaseExporter exporter = new BaseExporter();
        assertNotNull(exporter.getTemplateDir());
    }
}