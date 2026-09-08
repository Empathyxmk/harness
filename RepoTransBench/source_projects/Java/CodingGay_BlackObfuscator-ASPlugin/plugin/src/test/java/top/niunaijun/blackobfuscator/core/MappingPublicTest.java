package top.niunaijun.blackobfuscator.core;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Map;

public class MappingPublicTest {

    @Test
    public void testPutAndGetDifferentData() {
        Mapping mapping = new Mapping();
        // Use different class/method/field names than existing tests
        String className = "top.example2024.NewClass";
        String obfClassName = "aBcD_PUBLIC";
        mapping.putClassMapping(className, obfClassName);
        assertEquals(obfClassName, mapping.getObfuscatedClassName(className));

        String methodName = "publicMethod2024()V";
        String obfMethodName = "m2024";
        mapping.putMethodMapping(className, methodName, obfMethodName);
        assertEquals(obfMethodName, mapping.getObfuscatedMethodName(className, methodName));
        
        String fieldName = "publicField2024";
        String obfFieldName = "f2024";
        mapping.putFieldMapping(className, fieldName, obfFieldName);
        assertEquals(obfFieldName, mapping.getObfuscatedFieldName(className, fieldName));
    }

    @Test
    public void testToMapDifferentData() {
        Mapping mapping = new Mapping();
        mapping.putClassMapping("ClassA2024", "XxYyZz");
        Map<String, String> classMap = mapping.getClassMapping();
        assertEquals("XxYyZz", classMap.get("ClassA2024"));
        // Ensure output is a Map, and contains the new mapping
        assertTrue(classMap.containsKey("ClassA2024"));
    }
}