package com.scrapinghub.adblockparser.publictests;

import com.scrapinghub.adblockparser.AdblockRule;
import com.scrapinghub.adblockparser.AdblockRules;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicParsing {
    private final List<String> rules = Arrays.asList(
        "/track.js$script",
        "/log.gif$image",
        "||adnetwork.com^$third-party",
        "@@||safe.com/banner.gif$image"
    );
    private final AdblockRules adp = new AdblockRules(rules);

    @Test
    public void testPublicBlockScript() {
        Map<String, Boolean> paramsScript = new HashMap<>();
        paramsScript.put("script", true);
        assertTrue(adp.shouldBlock("http://another.com/track.js", paramsScript));
        Map<String, Boolean> paramsImage = new HashMap<>();
        paramsImage.put("image", true);
        assertFalse(adp.shouldBlock("http://another.com/track.js", paramsImage));
    }

    @Test
    public void testPublicBlockImage() {
        Map<String, Boolean> params = new HashMap<>();
        params.put("image", true);
        assertFalse(adp.shouldBlock("http://foo.com/track.gif", params));
        assertTrue(adp.shouldBlock("http://foo.com/log.gif", params));
    }

    @Test
    public void testPublicThirdParty() {
        Map<String, Boolean> params = new HashMap<>();
        params.put("third-party", true);
        assertFalse(adp.shouldBlock("http://x.yz/ad.js", params));
        assertTrue(adp.shouldBlock("http://adnetwork.com/adv_banner.jpg", params));
    }

    @Test
    public void testPublicException() {
        Map<String, Boolean> params = new HashMap<>();
        params.put("image", true);
        assertFalse(adp.shouldBlock("http://safe.com/banner.gif", params));
    }
}