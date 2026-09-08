package com.example.public_tests;

import com.example.alias_tips.AliasTips;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicAliasTips {
    // Test all known direct matches but reversed wordings and capitalization: should not match!
    @Test
    public void testSuggestAliasKnownVariants() {
        assertNull(AliasTips.suggestAlias("List"));       // different case
        assertNull(AliasTips.suggestAlias("Remove files"));  // superstring
        assertNull(AliasTips.suggestAlias("directory make")); // word order
        assertNull(AliasTips.suggestAlias("MOVE"));       // uppercase
    }

    // Test for alternate known commands (with spacing, extra words) that should not return an alias
    @Test
    public void testSuggestAliasNoneVariants() {
        assertNull(AliasTips.suggestAlias(" list "));     // leading/trailing space
        assertNull(AliasTips.suggestAlias("copy files")); // superstring
        assertNull(AliasTips.suggestAlias("Make Directory")); // casing
        assertNull(AliasTips.suggestAlias("mv"));         // alias itself
        assertNull(AliasTips.suggestAlias(0));            // another type
        assertNull(AliasTips.suggestAlias(new java.util.HashMap<>())); // another type
    }

    // Test is_alias_recommended positive on exact string, negative variants
    @Test
    public void testIsAliasRecommendedTrueAndFalse() {
        // Only exact string in right case should return True
        assertTrue(AliasTips.isAliasRecommended("move"));
        assertTrue(AliasTips.isAliasRecommended("copy"));

        assertFalse(AliasTips.isAliasRecommended("Move"));         // casing
        assertFalse(AliasTips.isAliasRecommended("copy file"));    // superstring
        assertFalse(AliasTips.isAliasRecommended("make  directory")); // extra space
        assertFalse(AliasTips.isAliasRecommended("ls"));           // alias itself
        assertFalse(AliasTips.isAliasRecommended(new java.util.HashMap<>()));             // wrong type
        assertFalse(AliasTips.isAliasRecommended(999));            // int
    }
}