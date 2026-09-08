package com.example.venmobusinessrules.original;

import com.example.venmobusinessrules.variables.BaseVariables;
import com.example.venmobusinessrules.variables.RuleVariable;
import com.example.venmobusinessrules.operators.StringType;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class VariablesClassTests {

    public static class DummyBaseVariables extends BaseVariables {}

    @Test
    public void testBaseHasNoVariables() {
        assertEquals(0, DummyBaseVariables.getAllVariables().size());
    }

    @Test
    public void testGetAllVariables() {
        class SomeVariables extends BaseVariables {
            @RuleVariable(type = StringType.class)
            public String publicRule1() {
                return "foo";
            }

            public String privateHelper() {
                return "no";
            }
        }

        List<Map<String, Object>> vars = SomeVariables.getAllVariables();
        assertEquals(1, vars.size());
        assertEquals("public_rule_1", vars.get(0).get("name"));
        assertEquals("Public Rule 1", vars.get(0).get("label"));
        assertEquals("string", vars.get(0).get("field_type"));
        assertEquals(List.of(), vars.get(0).get("options"));
    }
}