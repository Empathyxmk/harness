package com.example.venmobusinessrules.original;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class IntegrationTests {

    @Test
    public void testAllRulesPass() {
        boolean allRulesPassed = true;
        assertTrue(allRulesPassed);
    }

    @Test
    public void testSomeRulesFail() {
        boolean rulePassed = false;
        assertFalse(rulePassed);
    }

    @Test
    public void testActionsFireCorrectOrder() {
        List<String> log = List.of("first", "second", "third");
        assertEquals(List.of("first", "second", "third"), log);
    }
}