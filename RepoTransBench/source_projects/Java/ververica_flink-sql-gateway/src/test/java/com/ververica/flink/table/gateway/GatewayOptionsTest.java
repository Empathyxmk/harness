package com.ververica.flink.table.gateway;

import org.junit.jupiter.api.Test;

import java.net.URL;
import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class GatewayOptionsTest {

    @Test
    public void testOptionsWithNulls() {
        GatewayOptions opts = new GatewayOptions(true, null, null, null, null);
        assertTrue(opts.isPrintHelp());
        assertFalse(opts.getPort().isPresent());
        assertFalse(opts.getDefaultConfig().isPresent());
        assertEquals(Collections.emptyList(), opts.getJars());
        assertEquals(Collections.emptyList(), opts.getLibraryDirs());
    }

    @Test
    public void testOptionsWithValues() throws Exception {
        URL dummyUrl = new URL("file:/tmp/test1.jar");
        GatewayOptions opts = new GatewayOptions(false, 8081, dummyUrl, Arrays.asList(dummyUrl), Arrays.asList(dummyUrl));
        assertFalse(opts.isPrintHelp());
        assertEquals(8081, opts.getPort().get());
        assertEquals(dummyUrl, opts.getDefaultConfig().get());
        assertEquals(Arrays.asList(dummyUrl), opts.getJars());
        assertEquals(Arrays.asList(dummyUrl), opts.getLibraryDirs());
    }
}