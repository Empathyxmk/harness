package com.example.homu.original;

import com.example.homu.main.Main;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PrBodyTest {

    @Test
    public void testPrBodyContains() {
        String body = "Closes #42\nFixes issues";
        assertTrue(Main.prBodyContains(body, "Fixes"));
        assertFalse(Main.prBodyContains(body, "missing"));
    }

    @Test
    public void testSuppressPingsInPRBody() {
        String body = "r? @matklad\n" + "@bors r+\n" + "mail@example.com";
        String expect = "r? `@matklad`\n" + "`@bors` r+\n" + "mail@example.com\n";
        assertEquals(expect, Main.suppressPings(body));
    }

    @Test
    public void testSuppressIgnoreBlockInPRBody() {
        String body = "Rollup merge\n"
                + Main.IGNORE_BLOCK_START + "\n"
                + "[Create a similar rollup](https://fake.xyz/?prs=1,2,3)\n"
                + Main.IGNORE_BLOCK_END;
        String expect = "Rollup merge\n";
        assertEquals(expect, Main.suppressIgnoreBlock(body));
    }
}