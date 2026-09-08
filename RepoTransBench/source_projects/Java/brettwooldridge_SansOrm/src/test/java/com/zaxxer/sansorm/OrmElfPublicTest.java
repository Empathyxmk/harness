package com.zaxxer.sansorm;

import com.zaxxer.sansorm.internal.OrmBase;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class OrmElfPublicTest {

    @Test
    public void testUnderlineToCamelPublic() {
        // DIFFERENT test data than original
        assertEquals("snakeCaseField", OrmBase.underlineToCamel("snake_case_field"));
        assertEquals("anotherExample", OrmBase.underlineToCamel("another_example"));
        assertEquals("simpleTest", OrmBase.underlineToCamel("simple_test"));
    }

    @Test
    public void testCamelToUnderlinePublic() {
        // DIFFERENT test data than original
        assertEquals("user_name", OrmBase.camelToUnderline("userName"));
        assertEquals("test_data", OrmBase.camelToUnderline("testData"));
        assertEquals("red_blue_green", OrmBase.camelToUnderline("redBlueGreen"));
    }

    @Test
    public void testJoinPublic() {
        List<String> items = Arrays.asList("a", "b", "c");
        assertEquals("a,b,c", OrmBase.join(items, ","));
        assertEquals("a|b|c", OrmBase.join(items, "|"));
        assertEquals("abc", OrmBase.join(items, ""));
    }
}