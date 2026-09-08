package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.export.SupervisordExporter;

class TestExportSupervisord {

    @Test
    void testSupervisordSection() {
        SupervisordExporter exporter = new SupervisordExporter();
        String section = exporter.getSectionName("worker");
        assertEquals("[program:worker]", section);
    }
}