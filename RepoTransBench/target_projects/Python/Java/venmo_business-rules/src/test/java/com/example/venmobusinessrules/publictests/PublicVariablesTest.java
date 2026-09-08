package com.example.venmobusinessrules.publictests;

import com.example.venmobusinessrules.variables.BaseVariables;
import com.example.venmobusinessrules.variables.RuleVariable;
import com.example.venmobusinessrules.operators.StringType;
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

public class PublicVariablesTest {

    public static class DummyBaseVariables extends BaseVariables {}

    @Test
    public void testBaseVariablesHasNoVariables() {
        assertEquals(0, DummyBaseVariables.getAllVariables().size());
    }

    @Test
    public void testGetAllVariables() {
        class MyVariables extends BaseVariables {
            @RuleVariable(type = StringType.class)
            public String fooVar() { return "bar"; }
            public String helper() { return "no"; }
        }
        List<Map<String, Object>> vars = MyVariables.getAllVariables();
        assertEquals(1, vars.size());
        assertEquals("foo_var", vars.get(0).get("name"));
        assertEquals("Foo Var", vars.get(0).get("label"));
        assertEquals("string", vars.get(0).get("field_type"));
        assertEquals(List.of(), vars.get(0).get("options"));
    }
}