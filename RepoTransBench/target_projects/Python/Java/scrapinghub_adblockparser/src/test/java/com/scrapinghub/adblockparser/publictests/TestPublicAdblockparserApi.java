package com.scrapinghub.adblockparser.publictests;

import com.scrapinghub.adblockparser.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicAdblockparserApi {
    @Test
    public void testPublicImportsAvailable() {
        assertNotNull(new AdblockRules(new java.util.ArrayList<>()));
        assertNotNull(new AdblockRule("/ad.js"));
        assertThrows(AdblockParsingError.class, () -> { throw new AdblockParsingError("test"); });
    }
}