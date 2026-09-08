package com.ververica.flink.table.gateway;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.net.URL;

public class GatewayOptionsParserPublicTest {
    @Test
    public void testPrintHelpDoesNotThrowPublic() {
        assertDoesNotThrow(GatewayOptionsParser::printHelp);
    }

    @Test
    public void testParseHelpOptionLong() {
        String[] args = {"--help"};
        GatewayOptions opts = GatewayOptionsParser.parseGatewayOptions(args);
        assertTrue(opts.isPrintHelp());
    }

    @Test
    public void testParseWithDifferentPortAndDefaults() throws Exception {
        String testResource = "/test-sql-gateway-configuration.yaml";
        String defaultFilePath = getClass().getResource(testResource).toExternalForm();
        String[] args = {"-p", "9999", "-d", defaultFilePath};
        GatewayOptions opts = GatewayOptionsParser.parseGatewayOptions(args);
        assertEquals(9999, opts.getPort().get().intValue());
        assertTrue(opts.getDefaultConfig().isPresent());
        assertTrue(opts.getDefaultConfig().get().toString().contains("test-sql-gateway-configuration.yaml"));
    }

    @Test
    public void testParseWithNegativePort() {
        String[] args = {"-p", "-42"};
        GatewayOptions opts = GatewayOptionsParser.parseGatewayOptions(args);
        // GatewayOptionsParser accepts port argument as Integer, negative is valid format-wise
        // Let's check the value is set as negative
        assertEquals(-42, opts.getPort().get().intValue());
    }
}