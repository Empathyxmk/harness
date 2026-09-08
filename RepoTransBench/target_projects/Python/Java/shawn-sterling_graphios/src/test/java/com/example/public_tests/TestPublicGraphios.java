package com.example.public_tests;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

import com.example.graphios.Graphios;

public class TestPublicGraphios {

    @Test
    public void testPublicCreateMetricLine() {
        String line = Graphios.create_metric_line("disk_usage", "server3", "DiskIO", "write", 0.99, 456, 678, "2024-02-10 08:00:00");
        assertEquals("disk_usage,server3,DiskIO,write,0.99,456,678,2024-02-10 08:00:00", line);
    }

    @Test
    public void testPublicParseValue() {
        assertEquals(52.34, (double) Graphios.parse_value("52.34"), 1e-5);
        assertEquals("off", Graphios.parse_value("off"));
    }

    @Test
    public void testPublicFormatPerfdata() {
        Map<String, Object> pd = new HashMap<>();
        pd.put("label", "free_mem");
        pd.put("value", 1234);
        pd.put("uom", "MB");
        pd.put("warn", "");
        pd.put("crit", "");
        pd.put("min", 128);
        pd.put("max", 4096);
        String result = Graphios.format_perfdata(pd);
        assertTrue(result.startsWith("'free_mem'=1234MB;;;128;4096"));
    }

    @Test
    public void testPublicSplitPerfdata() {
        String perfdata = "'cpu'=15%;20;30;0;100 'mem'=4096MB;;;128;16384";
        java.util.List<Map<String, Object>> pd_list = Graphios.split_perfdata(perfdata);
        assertEquals("mem", pd_list.get(1).get("label"));
        assertEquals(4096, ((Number)pd_list.get(1).get("value")).intValue());
        assertEquals("MB", pd_list.get(1).get("uom"));
    }

    @Test
    public void testPublicStripPerfLabel() {
        assertEquals("swap", Graphios.strip_perf_label("'swap'"));
        assertEquals("disk", Graphios.strip_perf_label("disk"));
    }

    @Test
    public void testPublicIsNumeric() {
        assertTrue(Graphios.is_numeric("483.3"));
        assertFalse(Graphios.is_numeric("test998"));
    }

    @Test
    public void testPublicPerfdata2list() {
        String pd = "'io_read'=1MB 'io_write'=2MB;;;0;100";
        java.util.List<Map<String, Object>> res = Graphios.perfdata2list(pd);
        assertEquals("io_read", res.get(0).get("label"));
        assertEquals("io_write", res.get(1).get("label"));
    }
}