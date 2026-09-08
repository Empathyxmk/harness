package com.example.original;

import com.example.pdfredactor.RedactorOptions;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.function.Function;

public class TestRedactorOptions {

    @Test
    public void testOptionsDefaults() {
        RedactorOptions opts = new RedactorOptions();
        assertNull(opts.inputStream);
        assertNull(opts.outputStream);
        assertNotNull(opts.metadataFilters);
        assertEquals(0, opts.metadataFilters.size());
        assertNotNull(opts.xmpFilters);
        assertEquals(0, opts.xmpFilters.size());
        assertNull(opts.xmpSerializer);
        assertNotNull(opts.contentFilters);
        assertEquals(0, opts.contentFilters.size());
        assertNotNull(opts.contentReplacementGlyphs);
        assertEquals(List.of("?", "#", "*", " "), opts.contentReplacementGlyphs);
        assertNotNull(opts.linkFilters);
        assertEquals(0, opts.linkFilters.size());
    }

    @Test
    public void testSettingOptions() {
        RedactorOptions opts = new RedactorOptions();
        opts.inputStream = null; // in proper test could use ByteArrayInputStream
        opts.outputStream = null; // in proper test could use ByteArrayOutputStream

        opts.metadataFilters = new HashMap<>();
        opts.metadataFilters.put("Title", List.of((Function<String, String>)v -> "NewTitle"));
        opts.contentFilters = List.of();
        opts.linkFilters = List.of((Object...args) -> null);
        opts.xmpFilters = List.of(o -> null);
        opts.xmpSerializer = o -> "<xml />";

        assertNull(opts.inputStream);
        assertNull(opts.outputStream);
        assertTrue(opts.metadataFilters.get("Title").get(0) instanceof Function);
        assertNull(opts.linkFilters.get(0).apply(new Object[]{"href", null}));
        assertNull(opts.xmpFilters.get(0).apply(null));
        assertEquals("<xml />", opts.xmpSerializer.apply(null));
    }
}