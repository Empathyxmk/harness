package to.lean.tools.gmail.importer.local.thunderbird;

import org.junit.Test;
import static org.junit.Assert.*;

public class ThunderbirdLocalMessagePublicTest {

    @Test
    public void testDifferentMessageIdDefaultFolder() {
        ThunderbirdLocalMessage msg = new ThunderbirdLocalMessage("xyz789", "public_folder");
        assertEquals("xyz789", msg.getMessageId());
        assertTrue(msg.getFolders().contains("public_folder"));
    }
}