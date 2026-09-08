package com.zfkun.plugins.mymap;

import com.janetfilter.core.enums.RuleType;
import com.janetfilter.core.models.FilterRule;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class PutFilterPublicTest {

    @Test
    public void testAllowWithNullRules_public() {
        PutFilter putFilter = new PutFilter(null);
        assertTrue(putFilter.shouldAllow("someKey"));
    }

    @Test
    public void testAllowWithEmptyRules_public() {
        PutFilter putFilter = new PutFilter(Collections.emptyList());
        assertTrue(putFilter.shouldAllow("anotherKey"));
    }

    @Test
    public void testAllowWithNullKey_public() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "foo");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertTrue(putFilter.shouldAllow(null));
    }

    @Test
    public void testBlockEqualRule_public() {
        FilterRule rule = new FilterRule(RuleType.EQUAL, "deny");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertFalse(putFilter.shouldAllow("deny"));
        assertTrue(putFilter.shouldAllow("DENY"));  // still case-sensitive
    }

    @Test
    public void testBlockContainsRule_public() {
        FilterRule rule = new FilterRule(RuleType.CONTAINS, "testz");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertFalse(putFilter.shouldAllow("exec_testz_helper"));
        assertTrue(putFilter.shouldAllow("basic_helper"));
    }

    @Test
    public void testAllowWithUnknownType_public() {
        FilterRule rule = new FilterRule(null, "nothing");
        PutFilter putFilter = new PutFilter(Collections.singletonList(rule));
        assertTrue(putFilter.shouldAllow("nothing"));
    }

    @Test
    public void testAllowWithNullRule_public() {
        PutFilter putFilter = new PutFilter(Arrays.asList(
                null,
                new FilterRule(RuleType.EQUAL, null)
        ));
        assertTrue(putFilter.shouldAllow("foobar"));
    }

    @Test
    public void testMultipleRules_public() {
        FilterRule r1 = new FilterRule(RuleType.EQUAL, "firsty");
        FilterRule r2 = new FilterRule(RuleType.CONTAINS, "r3d");
        PutFilter putFilter = new PutFilter(Arrays.asList(r1, r2));
        assertFalse(putFilter.shouldAllow("firsty"));
        assertFalse(putFilter.shouldAllow("meshr3dmesh"));
        assertTrue(putFilter.shouldAllow("totallyDifferent"));
    }
}