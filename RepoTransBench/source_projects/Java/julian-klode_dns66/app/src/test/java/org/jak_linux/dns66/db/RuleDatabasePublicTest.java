package org.jak_linux.dns66.db;

import org.junit.Test;
import static org.junit.Assert.*;

public class RuleDatabasePublicTest {

    @Test
    public void testTypeConstantsPublic() {
        assertEquals(0, RuleDatabase.TYPE_HOSTS);
        assertEquals(1, RuleDatabase.TYPE_DNS);
        assertEquals(2, RuleDatabase.TYPE_ALLOWLIST);
    }

    @Test
    public void testConstructRuleDatabaseItemPublic() {
        RuleDatabase.RuleDatabaseItem item = new RuleDatabase.RuleDatabaseItem();
        item.title = "publicTitle";
        item.enabled = true;
        item.url = "publicUrl";
        item.type = RuleDatabase.TYPE_DNS;

        assertEquals("publicTitle", item.title);
        assertTrue(item.enabled);
        assertEquals("publicUrl", item.url);
        assertEquals(RuleDatabase.TYPE_DNS, item.type);
    }

}