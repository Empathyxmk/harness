package org.cas.public_tests;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

class PublicTestCASUncovered {
    @Test
    @Disabled("Test requires network access; skipping public variant as well.")
    void testGetProxyTicketCustomPublic() {
        // Skipped in public tests; mirrors skip in private test.
    }

    @Test
    @Disabled("Test requires network access; skipping public variant as well.")
    void testSomeOtherNetworkTestPublic() {
        // Skipped in public tests; mirrors skip in private test.
    }
}