package com.scrapinghub.adblockparser.publictests;

import com.scrapinghub.adblockparser.AdblockRule;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicOptions {
    @Test
    public void testPublicParseOptionsSimple() {
        AdblockRule r = new AdblockRule("/ad.js$script,domain=example.com|another.net");
        assertTrue(r.options.containsKey("script"));
        assertTrue(r.options.containsKey("domain"));
        assertEquals(new HashSet<>(Arrays.asList("example.com", "another.net")), r.options.get("domain"));
    }

    @Test
    public void testPublicParseOptionsNoOptions() {
        AdblockRule r = new AdblockRule("/track.gif");
        assertEquals(Collections.emptyMap(), r.options);
    }

    @Test
    public void testPublicParseOptionsComplex() {
        AdblockRule r = new AdblockRule("/analytics.js$image,third-party,domain=mysite.org|anothersite.co.uk");
        assertTrue(r.options.containsKey("image"));
        assertTrue(r.options.containsKey("third-party"));
        assertEquals(new HashSet<>(Arrays.asList("mysite.org", "anothersite.co.uk")), r.options.get("domain"));
    }

    @Test
    public void testPublicParseOptionsException() {
        AdblockRule r = new AdblockRule("@@/nocache.png$subdocument,domain=sub.example.org");
        assertTrue(r.isException);
        assertTrue(r.options.containsKey("subdocument"));
        assertEquals(new HashSet<>(Arrays.asList("sub.example.org")), r.options.get("domain"));
    }
}