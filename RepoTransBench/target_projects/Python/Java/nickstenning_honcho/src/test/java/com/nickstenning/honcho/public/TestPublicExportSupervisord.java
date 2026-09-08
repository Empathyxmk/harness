package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.SupervisordExporter;

class TestPublicExportSupervisord {

    @Test
    void testPublicSupervisordSectionName() {
        SupervisordExporter exporter = new SupervisordExporter();
        String section = exporter.getSectionName("worker");
        assertEquals("[program:worker]", section);
    }
}