package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class FileMeta {
    String id;
    String name;
    long sizeBytes;
    public FileMeta(String id, String name, long sizeBytes) {
        this.id = id;
        this.name = name;
        this.sizeBytes = sizeBytes;
    }
}

public class PublicFilesTest {
    @Test
    void testFileMetaInit() {
        FileMeta f = new FileMeta("f55", "report.pdf", 10240);
        assertEquals("f55", f.id);
        assertEquals("report.pdf", f.name);
        assertEquals(10240, f.sizeBytes);
    }

    @Test
    void testFileMetaLargeFile() {
        FileMeta f = new FileMeta("f999", "huge.zip", 1024L * 1024L * 100L);
        assertTrue(f.sizeBytes > 1_000_000);
        assertEquals("huge.zip", f.name);
    }
}