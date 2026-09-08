package org.jak_linux.dns66.db;

import org.jak_linux.dns66.db.RuleDatabase.RuleDatabaseItem;
import org.junit.Test;

import static org.junit.Assert.*;

public class RuleDatabaseItemUpdateRunnablePublicTest {

    @Test
    public void testRuleDatabaseItemSetEnabledPublic() {
        // Use different values/entities
        RuleDatabaseItem item = new RuleDatabaseItem();
        item.enabled = false;
        item.url = "public_test_url";
        item.title = "PublicTitle";
        item.type = RuleDatabase.TYPE_ALLOWLIST;

        // test enabling
        item.enabled = true;
        assertTrue(item.enabled);

        // test data is preserved
        assertEquals("public_test_url", item.url);
        assertEquals("PublicTitle", item.title);
        assertEquals(RuleDatabase.TYPE_ALLOWLIST, item.type);
    }
}