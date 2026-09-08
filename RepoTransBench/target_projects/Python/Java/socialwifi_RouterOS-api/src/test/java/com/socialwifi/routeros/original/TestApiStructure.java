package com.socialwifi.routeros.original;

import com.socialwifi.routeros.api_structure.ApiStructure;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

class TestApiStructure {

    @Test
    void testGetSubresource() {
        ApiStructure structure = new ApiStructure();
        structure.addResource("/interface/wifi");
        ApiStructure sub = structure.getSubresource("/interface/wifi");
        assertNotNull(sub);
        assertEquals("/interface/wifi", sub.getName());
    }

    @Test
    void testListSubresources() {
        ApiStructure structure = new ApiStructure();
        structure.addResource("/interface/eth");
        structure.addResource("/interface/wifi");
        assertTrue(structure.listSubresources("/interface").contains("/interface/eth"));
        assertTrue(structure.listSubresources("/interface").contains("/interface/wifi"));
    }

    @Test
    void testFieldDefinitions() {
        ApiStructure structure = new ApiStructure();
        structure.addResource("/interface");
        structure.addField("/interface", "name", "string");
        structure.addField("/interface", "type", "string");

        Map<String, String> fields = structure.getFieldDefinitions("/interface");
        assertEquals("string", fields.get("name"));
        assertEquals("string", fields.get("type"));
    }
}