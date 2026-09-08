package com.scrapinghub.adblockparser.publictests;

import com.scrapinghub.adblockparser.AdblockRule;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicRuleTypes {
    static List<String> commentRules() {
        return Arrays.asList(
            "! This is a comment line",
            "! Title: Example Filter List",
            "! Expires: 4 days",
            "! Homepage: https://example.com/",
            "[Adblock]",
            "!#include another_list.txt"
        );
    }

    static List<String> htmlRules() {
        return Arrays.asList(
            "##.bannerAd",
            "@@##.sponsoredContent",
            "mysite.com#@##sidebar",
            "@@##.cookieBar",
            "example.net,example.org#@##promo",
            "##a[href^='https://tracker.example.com/']",
            "##img[src$=\".ads.png\"]"
        );
    }

    @ParameterizedTest
    @MethodSource("commentRules")
    public void testPublicIsComment(String text) {
        AdblockRule rule = new AdblockRule(text);
        assertTrue(rule.isComment);
        assertFalse(rule.isHtmlRule);
        assertFalse(rule.isException);
        assertEquals(Collections.emptyMap(), rule.options);
        assertNull(rule.regex);
    }

    @ParameterizedTest
    @MethodSource("htmlRules")
    public void testPublicIsHtmlRule(String text) {
        AdblockRule rule = new AdblockRule(text);
        assertTrue(rule.isHtmlRule);
        assertFalse(rule.isComment);
    }
}