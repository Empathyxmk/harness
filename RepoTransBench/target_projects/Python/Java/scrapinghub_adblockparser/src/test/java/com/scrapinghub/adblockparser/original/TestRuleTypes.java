package com.scrapinghub.adblockparser.original;

import com.scrapinghub.adblockparser.AdblockRule;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestRuleTypes {
    static List<String> commentRules() {
        return Arrays.asList(
            "[Adblock Plus 2.0]",
            "! Checksum: nVIXktYXKU6M+cu+Txkhuw",
            "!/cb.php?sub$script,third-party",
            "!@@/cb.php?sub",
            "!###ADSLOT_SKYSCRAPER",
            "! *** easylist:easylist/easylist_whitelist_general_hide.txt ***"
        );
    }

    static List<String> htmlRules() {
        return Arrays.asList(
            "###ADSLOT_SKYSCRAPER",
            "@@###ADSLOT_SKYSCRAPER",
            "##.adsBox",
            "eee.se#@##adspace_top",
            "domain1.com,domain2.com#@##adwrapper",
            "edgesuitedomain.net#@##ad-unit",
            "mydomain.com#@#.ad-unit",
            "##a[href^=\"http://affiliate.sometracker.com/\"]"
        );
    }

    @ParameterizedTest
    @MethodSource("commentRules")
    public void testIsComment(String text) {
        AdblockRule rule = new AdblockRule(text);
        assertTrue(rule.isComment);
        assertFalse(rule.isHtmlRule);
        assertFalse(rule.isException);
        assertEquals(Collections.emptyMap(), rule.options);
        assertNull(rule.regex);
    }

    @ParameterizedTest
    @MethodSource("htmlRules")
    public void testIsHtmlRule(String text) {
        AdblockRule rule = new AdblockRule(text);
        assertTrue(rule.isHtmlRule);
        assertFalse(rule.isComment);
    }
}