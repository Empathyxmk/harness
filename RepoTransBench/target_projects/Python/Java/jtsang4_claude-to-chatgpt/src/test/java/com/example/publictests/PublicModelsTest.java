package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicModelsTest {

    @Test
    public void testPublicModelsListExists() {
        List<String> modelsList = PublicModelsMockData.modelsList;
        assertNotNull(modelsList);
        assertTrue(modelsList instanceof List);
        for (Object item : modelsList) {
            assertTrue(item instanceof String);
        }
    }

    @Test
    public void testPublicModelMapExists() {
        Map<String, String> modelMap = PublicModelsMockData.modelMap;
        assertNotNull(modelMap);
        assertTrue(modelMap instanceof Map);
        for (Map.Entry<String, String> entry : modelMap.entrySet()) {
            assertTrue(entry.getKey() instanceof String && entry.getValue() instanceof String);
        }
    }
}

class PublicModelsMockData {
    public static List<String> modelsList = Arrays.asList("model1public","model2public");
    public static Map<String,String> modelMap = Map.of(
        "gpt-3.5-turbo-0613", "claude-2", 
        "gpt-4-0314", "claude-v1"
    );
}