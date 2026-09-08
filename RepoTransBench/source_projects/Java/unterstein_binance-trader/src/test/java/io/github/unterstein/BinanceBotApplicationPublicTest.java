package io.github.unterstein;

import org.junit.jupiter.api.Test;

class BinanceBotApplicationPublicTest {

    @Test
    void testMainRunsWithArgs() {
        // Test with some dummy command-line args (different from existing empty args)
        BinanceBotApplication.main(new String[] {"--simulate", "--config=test.properties"});
    }
}