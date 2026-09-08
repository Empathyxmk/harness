package com.seatgeek.public_tests;

import com.seatgeek.fuzzywuzzy.Utils;
import com.seatgeek.fuzzywuzzy.StringMatcher;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsAndStringMatcherTest {
    @Test
    void testAsciidammitPublic() {
        String s = "Café Noël Über ß";
        String result = Utils.asciidammit(s);
        assertNotNull(result);
        assertFalse(result.contains("\u00e9"));
    }

    @Test
    void testAsciionlyPublic() {
        String s = Utils.asciidammit("façade naïve jalapeño");
        String result = Utils.asciionly(s);
        for (char c : result.toCharArray()) {
            assertTrue("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ".indexOf(c) >= 0);
        }
    }

    @Test
    void testFullProcessPublic() {
        String s = "Fußball & Crème brûlée";
        String result = Utils.fullProcess(s);
        assertNotNull(result);
        assertFalse(result.contains("&"));
    }

    @Test
    void testStringmatcherRatioPublic() {
        String s1 = "hello";
        String s2 = "hullo";
        StringMatcher m = new StringMatcher();
        m.setSeq1(s1);
        m.setSeq2(s2);
        double ratio = m.ratio();
        assertTrue(ratio > 0.7);
        assertTrue(ratio < 1.0);
    }
}