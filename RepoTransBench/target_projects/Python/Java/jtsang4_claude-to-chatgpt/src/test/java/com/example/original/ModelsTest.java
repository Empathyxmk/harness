package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class ModelsTest {

    @Test
    public void testModelsListExists() {
        List<String> modelsList = ModelsMockData.modelsList;
        assertNotNull(modelsList);
        assertTrue(modelsList instanceof List);
    }

    @Test
    public void testModelMapExists() {
        Map<String,String> modelMap = ModelsMockData.modelMap;
        assertNotNull(modelMap);
        assertTrue(modelMap instanceof Map);
    }
}

class ModelsMockData {
    public static List<String> modelsList = Arrays.asList("model1","model2","model3");
    public static Map<String,String> modelMap = Map.of(
        "gpt-3.5-turbo-0613", "claude-2", 
        "gpt-4-0314", "claude-v1"
    );
}