package com.zfkun.plugins.mymap;

import com.janetfilter.core.enums.RuleType;
import com.janetfilter.core.models.FilterRule;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class MapTransformerTest {

    @Test
    public void testContainsRuleEqualMatch() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "test");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertTrue(transformer.containsRule("test"));
    }

    @Test
    public void testContainsRuleEqualNoMatch() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "hello");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("world"));
    }

    @Test
    public void testContainsRuleContainsMatch() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "abc");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertTrue(transformer.containsRule("123abc456"));
    }

    @Test
    public void testContainsRuleNullInput() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "abc");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule(null));
    }

    @Test
    public void testContainsRuleNullRuleType() {
        FilterRule rule = new FilterRule(null, "abc");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("abc"));
    }

    @Test
    public void testContainsRuleNullRule() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, null);
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("test"));
    }

    @Test
    public void testContainsRuleMultipleRules() {
        FilterRule r1 = new FilterRule(RuleType.CONTAINS, "foo");
        FilterRule r2 = new FilterRule(RuleType.EQUAL, "bar");
        MapTransformer transformer = new MapTransformer(Arrays.asList(r1, r2));
        assertTrue(transformer.containsRule("foobar"));
        assertTrue(transformer.containsRule("bar"));
        assertFalse(transformer.containsRule("baz"));
    }

    @Test
    public void testGetRules() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "abc");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertEquals(1, transformer.getRules().size());
    }
}