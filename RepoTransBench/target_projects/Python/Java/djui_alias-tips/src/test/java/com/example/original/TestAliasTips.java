package com.example.original;

import com.example.alias_tips.AliasTips;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestAliasTips {
    // Test all known direct matches
    @Test
    public void testSuggestAliasKnown() {
        assertEquals("ls", AliasTips.suggestAlias("list"));
        assertEquals("rm", AliasTips.suggestAlias("remove"));
        assertEquals("cp", AliasTips.suggestAlias("copy"));
        assertEquals("mv", AliasTips.suggestAlias("move"));
        assertEquals("mkdir", AliasTips.suggestAlias("make directory"));
    }

    // Test unrecognized commands and edge cases
    @Test
    public void testSuggestAliasNone() {
        assertNull(AliasTips.suggestAlias("unknown"));
        assertNull(AliasTips.suggestAlias(""));
        assertNull(AliasTips.suggestAlias(null));
        assertNull(AliasTips.suggestAlias(123));    // non-str input
        assertNull(AliasTips.suggestAlias(new java.util.ArrayList<>())); // non-str input
    }

    // Test is_alias_recommended positive
    @Test
    public void testIsAliasRecommendedTrue() {
        assertTrue(AliasTips.isAliasRecommended("list"));
        assertTrue(AliasTips.isAliasRecommended("remove"));
        assertTrue(AliasTips.isAliasRecommended("copy"));
        assertTrue(AliasTips.isAliasRecommended("move"));
        assertTrue(AliasTips.isAliasRecommended("make directory"));
    }

    // Test is_alias_recommended false
    @Test
    public void testIsAliasRecommendedFalse() {
        assertFalse(AliasTips.isAliasRecommended("something else"));
        assertFalse(AliasTips.isAliasRecommended(""));
        assertFalse(AliasTips.isAliasRecommended(null));
        assertFalse(AliasTips.isAliasRecommended(123));
        assertFalse(AliasTips.isAliasRecommended(new java.util.ArrayList<>()));
    }
}