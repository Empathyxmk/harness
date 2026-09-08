package com.zfkun.plugins.mymap;

import com.janetfilter.core.enums.RuleType;
import com.janetfilter.core.models.FilterRule;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class PutFilterTest {

    @Test
    public void testAllowWithNullRules() {
        PutFilter putFilter = new PutFilter(null);
        assertTrue(putFilter.shouldAllow("key"));
    }

    @Test
    public void testAllowWithEmptyRules() {
        PutFilter putFilter = new PutFilter(Collections.emptyList());
        assertTrue(putFilter.shouldAllow("key"));
    }

    @Test
    public void testAllowWithNullKey() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "bar");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertTrue(putFilter.shouldAllow(null));
    }

    @Test
    public void testBlockEqualRule() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "block");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertFalse(putFilter.shouldAllow("block"));
        assertTrue(putFilter.shouldAllow("BLOCK"));  // case-sensitive
    }

    @Test
    public void testBlockContainsRule() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "xyz");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertFalse(putFilter.shouldAllow("helloxyzworld"));
        assertTrue(putFilter.shouldAllow("helloworld"));
    }

    @Test
    public void testAllowWithUnknownType() {
        FilterRule rule = new FilterRule(null, "block");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertTrue(putFilter.shouldAllow("block"));
    }

    @Test
    public void testAllowWithNullRule() {
        PutFilter putFilter = new PutFilter(Arrays.asList(
                null,
                new FilterRule(RuleType.EQUAL, null)
        ));
        assertTrue(putFilter.shouldAllow("something"));
    }

    @Test
    public void testMultipleRules() {
        FilterRule r1 = new FilterRule(RuleType.EQUAL, "a");
        FilterRule r2 = new FilterRule(RuleType.CONTAINS, "bc");
        PutFilter putFilter = new PutFilter(Arrays.asList(r1, r2));
        assertFalse(putFilter.shouldAllow("a"));
        assertFalse(putFilter.shouldAllow("bcd"));
        assertTrue(putFilter.shouldAllow("xyz"));
    }
}