package to.lean.tools.gmail.importer.gmail;

import org.junit.Test;

import static org.junit.Assert.*;

public class GmailServiceModulePublicTest {

    @Test
    public void testDifferentProvidesMailboxName() {
        GmailServiceModule module = new GmailServiceModule("PublicMailboxName");
        assertEquals("PublicMailboxName", module.mailboxName);
    }
}