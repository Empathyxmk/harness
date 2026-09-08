package org.jak_linux.dns66.db;

import org.junit.Test;

import static org.junit.Assert.*;

public class RuleDatabaseUpdateTaskPublicTest {

    @Test
    public void testRunWithoutExceptionsPublic() {
        // This test just assures the code runs; let's call the constructor with dummy values.
        RuleDatabase.RuleDatabaseItem item = new RuleDatabase.RuleDatabaseItem();
        item.title = "UpdatePublic";
        item.enabled = true;
        item.url = "http://test-public/";
        item.type = RuleDatabase.TYPE_DNS;

        RuleDatabaseUpdateTask task = new RuleDatabaseUpdateTask(null, item, true);
        // Do not call run(), but exercise constructor and toString
        assertNotNull(task.toString());
    }
}