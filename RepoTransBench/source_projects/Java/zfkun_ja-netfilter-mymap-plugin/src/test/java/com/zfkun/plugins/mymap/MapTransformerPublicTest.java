package com.zfkun.plugins.mymap;

import com.janetfilter.core.enums.RuleType;
import com.janetfilter.core.models.FilterRule;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class MapTransformerPublicTest {

    @Test
    public void testContainsRuleEqualMatch_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "publicValue");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertTrue(transformer.containsRule("publicValue"));
    }

    @Test
    public void testContainsRuleEqualNoMatch_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "apple");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("orange"));
    }

    @Test
    public void testContainsRuleContainsMatch_public() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "uvw");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertTrue(transformer.containsRule("123uvwx456"));
    }

    @Test
    public void testContainsRuleNullInput_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "xyz");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule(null));
    }

    @Test
    public void testContainsRuleNullRuleType_public() {
        FilterRule rule = new FilterRule(null, "banana");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("banana"));
    }

    @Test
    public void testContainsRuleNullRule_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, null);
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertFalse(transformer.containsRule("AlphaTest"));
    }

    @Test
    public void testContainsRuleMultipleRules_public() {
        FilterRule r1 = new FilterRule(RuleType.CONTAINS, "abc");
        FilterRule r2 = new FilterRule(RuleType.EQUAL, "xyz123");
        MapTransformer transformer = new MapTransformer(Arrays.asList(r1, r2));
        assertTrue(transformer.containsRule("loremabcipso"));
        assertTrue(transformer.containsRule("xyz123"));
        assertFalse(transformer.containsRule("hello world"));
    }

    @Test
    public void testGetRules_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "public");
        MapTransformer transformer = new MapTransformer(Collections.singletonList(rule));
        assertEquals(1, transformer.getRules().size());
    }
}