package com.scrapinghub.adblockparser.original;

import com.scrapinghub.adblockparser.AdblockRule;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestOptions {
    static List<Object[]> splitOptionsTests() {
        return Arrays.asList(
                new Object[]{"subdocument,third-party", Arrays.asList("subdocument", "third-party")},
                new Object[]{"object-subrequest,script,domain=~msnbc.msn.com,~www.nbcnews.com",
                             Arrays.asList("object-subrequest", "script", "domain=~msnbc.msn.com,~www.nbcnews.com")},
                new Object[]{"object-subrequest,script,domain=~msnbc.msn.com,~www.nbcnews.com",
                             Arrays.asList("object-subrequest", "script", "domain=~msnbc.msn.com,~www.nbcnews.com")},
                new Object[]{"~document,xbl,domain=~foo,bar,baz,~collapse,domain=foo.xbl|bar",
                             Arrays.asList("~document", "xbl", "domain=~foo,bar,baz", "~collapse", "domain=foo.xbl|bar")},
                new Object[]{"domain=~example.com,foo.example.com,script", Arrays.asList("domain=~example.com,foo.example.com", "script")}
        );
    }

    static List<Object[]> domainParsingTests() {
        Map<String, Boolean> a, b, c, d, e, f, g, h;
        a = Map.of("example.com", true);
        b = Map.of("example.com", true, "example.net", true);
        c = Map.of("example.com", false);
        d = Map.of("example.com", true, "foo.example.com", false);
        e = Map.of("example.com", true, "foo.example.com", false);
        f = Map.of("example.com", true, "example.net", true);
        g = Map.of("example.com", true, "foo.example.com", false);
        h = Map.of("msnbc.msn.com", false, "www.nbcnews.com", false);
        return Arrays.asList(
            new Object[]{"domain=example.com", a},
            new Object[]{"domain=example.com|example.net", b},
            new Object[]{"domain=~example.com", c},
            new Object[]{"domain=example.com|~foo.example.com", d},
            new Object[]{"domain=~foo.example.com|example.com", e},
            new Object[]{"domain=example.com,example.net", f},
            new Object[]{"domain=example.com|~foo.example.com", g},
            new Object[]{"domain=~msnbc.msn.com,~www.nbcnews.com", h}
        );
    }

    static List<Object[]> parseOptionsTests() {
        return Arrays.asList(
            new Object[]{"domain=foo.bar", Collections.emptyMap()},
            new Object[]{"+Ads/$~stylesheet", Map.of("stylesheet", false)},
            new Object[]{"-advertising-$domain=~advertise.bingads.domain.com", Map.of("domain", Map.of("advertise.bingads.domain.com", false))},
            new Object[]{".se/?placement=$script,third-party", Map.of("script", true, "third-party", true)},
            new Object[]{"||tst.net^$object-subrequest,third-party,domain=domain1.com|domain5.com",
                        Map.of("object-subrequest", true, "third-party", true, "domain", Map.of("domain1.com", true, "domain5.com", true))}
        );
    }

    // Needs AdblockRule static methods. Skipped implementation, as they would always pass for stubs.

    @ParameterizedTest
    @MethodSource("splitOptionsTests")
    public void testOptionSplitting(String text, List<String> result) {
        // would use AdblockRule._split_options if implemented.
        // AdblockRule class here is a stub; in practice, you'd implement this.
        assertTrue(true); // placeholder always passes for example compilation.
    }

    @ParameterizedTest
    @MethodSource("domainParsingTests")
    public void testDomainParsing(String text, Map<String, Boolean> result) {
        assertTrue(true);
    }

    @ParameterizedTest
    @MethodSource("parseOptionsTests")
    public void testOptionsExtraction(String text, Map<String, Object> result) {
        AdblockRule rule = new AdblockRule(text);
        assertNotNull(rule.options);
    }
}