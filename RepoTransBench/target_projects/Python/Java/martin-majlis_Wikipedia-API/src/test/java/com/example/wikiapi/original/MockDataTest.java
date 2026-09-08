package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;

class MockDataTest {
    @Test
    void testGetMockDataForPageNames() {
        List<String> pageNames = Arrays.asList("Test_1", "Test_2", "Test_3");
        for (String name : pageNames) {
            Map<String, Object> data = WikipediaApi.MockData.getMockData(name);
            assertNotNull(data);
            assertEquals(name, data.get("title"));
        }
    }
}