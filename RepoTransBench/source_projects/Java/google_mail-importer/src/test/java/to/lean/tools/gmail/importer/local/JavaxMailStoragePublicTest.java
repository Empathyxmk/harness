package to.lean.tools.gmail.importer.local;

import org.junit.Test;
import javax.mail.Flags;
import javax.mail.internet.MimeMessage;
import javax.mail.Session;

import java.util.Properties;

import static org.junit.Assert.*;

public class JavaxMailStoragePublicTest {

    @Test
    public void testCreateFlagDifferentInput() throws Exception {
        Flags flags = new Flags();
        flags.add(Flags.Flag.DRAFT);
        MimeMessage msg = new MimeMessage((Session)null);
        JavaxMailStorage.addFlags(msg, flags);
        assertTrue(msg.getFlags().contains(Flags.Flag.DRAFT));
    }
}