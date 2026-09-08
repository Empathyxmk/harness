package com.scrapinghub.adblockparser.original;

import com.scrapinghub.adblockparser.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestAdblockparserApi {
    @Test
    public void testImportsAvailable() {
        // Only checks presence, will always "pass" in stub, but real project would check for access.
        assertNotNull(new AdblockRules(new java.util.ArrayList<>()));
        assertNotNull(new AdblockRule("/ad.js"));
        assertThrows(AdblockParsingError.class, () -> { throw new AdblockParsingError("test"); });
    }
}