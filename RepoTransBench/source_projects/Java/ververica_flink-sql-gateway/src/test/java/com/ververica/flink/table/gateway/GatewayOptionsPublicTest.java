package com.ververica.flink.table.gateway;

import org.junit.jupiter.api.Test;

import java.net.URL;
import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class GatewayOptionsPublicTest {

    @Test
    public void testOptionsWithEmptyListValues() {
        GatewayOptions opts = new GatewayOptions(false, null, null, Collections.emptyList(), Collections.emptyList());
        assertFalse(opts.isPrintHelp());
        assertFalse(opts.getPort().isPresent());
        assertFalse(opts.getDefaultConfig().isPresent());
        assertEquals(Collections.emptyList(), opts.getJars());
        assertEquals(Collections.emptyList(), opts.getLibraryDirs());
    }

    @Test
    public void testOptionsWithDifferentValues() throws Exception {
        URL dummyUrl = new URL("file:/tmp/publictest2.jar");
        GatewayOptions opts = new GatewayOptions(true, 9090, dummyUrl, Arrays.asList(dummyUrl), Arrays.asList(dummyUrl));
        assertTrue(opts.isPrintHelp());
        assertEquals(9090, opts.getPort().get());
        assertEquals(dummyUrl, opts.getDefaultConfig().get());
        assertEquals(Arrays.asList(dummyUrl), opts.getJars());
        assertEquals(Arrays.asList(dummyUrl), opts.getLibraryDirs());
    }
}