package com.ververica.flink.table.gateway;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.net.URL;

public class GatewayOptionsParserTest {
    @Test
    public void testPrintHelpDoesNotThrow() {
        assertDoesNotThrow(GatewayOptionsParser::printHelp);
    }

    @Test
    public void testParseHelpOption() {
        String[] args = {"-h"};
        GatewayOptions opts = GatewayOptionsParser.parseGatewayOptions(args);
        assertTrue(opts.isPrintHelp());
    }

    @Test
    public void testParseWithPortAndDefaults() throws Exception {
        String defaultFilePath = getClass().getResource("/test-sql-gateway-defaults.yaml").toExternalForm();
        String[] args = {"-p", "8888", "-d", defaultFilePath};
        GatewayOptions opts = GatewayOptionsParser.parseGatewayOptions(args);
        assertEquals(8888, opts.getPort().get().intValue());
        assertTrue(opts.getDefaultConfig().isPresent());
        assertTrue(opts.getDefaultConfig().get().toString().contains("test-sql-gateway-defaults.yaml"));
    }

    @Test
    public void testParseWithInvalidPort() {
        String[] args = {"-p", "not_a_number"};
        Exception ex = assertThrows(com.ververica.flink.table.gateway.utils.SqlGatewayException.class, () -> {
            GatewayOptionsParser.parseGatewayOptions(args);
        });
        assertTrue(ex.getMessage().toLowerCase().contains("for input string"));
    }
}