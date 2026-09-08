package com.example.venmobusinessrules.publictests;

import com.example.venmobusinessrules.operators.BaseType;
import com.example.venmobusinessrules.operators.TypeOperator;
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

public class PublicOperatorsClassTest {

    public static class DummyBaseType extends BaseType {}

    @Test
    public void testBaseTypeHasNoOperators() {
        assertEquals(0, DummyBaseType.getAllOperators().size());
    }

    @Test
    public void testGetAllOperators() {
        class MyType extends BaseType {
            @TypeOperator(inputType = "text")
            public boolean myOp() { return true; }
            public boolean helper() { return false; }
        }

        List<Map<String, Object>> operators = MyType.getAllOperators();
        assertEquals(1, operators.size());
        assertEquals("my_op", operators.get(0).get("name"));
        assertEquals("My Op", operators.get(0).get("label"));
        assertEquals("text", operators.get(0).get("input_type"));
    }
}