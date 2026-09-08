package com.example.venmobusinessrules.original;

import com.example.venmobusinessrules.actions.BaseActions;
import com.example.venmobusinessrules.actions.RuleAction;
import com.example.venmobusinessrules.fields.Fields;
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

public class ActionsClassTests {

    public static class DummyBaseActions extends BaseActions {}

    @Test
    public void testBaseHasNoActions() {
        assertEquals(0, DummyBaseActions.getAllActions().size());
    }

    @Test
    public void testGetAllActionsWithParamsAndLabels() {
        class MyActions extends BaseActions {
            @RuleAction(params = @RuleAction.Param(name = "foo", fieldType = Fields.FIELD_TEXT))
            public String fooAction(String foo) { return foo + " bar"; }

            public String helper() { return "no"; }
        }

        List<Map<String, Object>> actions = MyActions.getAllActions();
        assertEquals(1, actions.size());
        assertEquals("foo_action", actions.get(0).get("name"));
        assertEquals("Foo Action", actions.get(0).get("label"));
        assertEquals(List.of(
                Map.of("fieldType", Fields.FIELD_TEXT, "name", "foo", "label", "Foo")
        ), actions.get(0).get("params"));
    }
}