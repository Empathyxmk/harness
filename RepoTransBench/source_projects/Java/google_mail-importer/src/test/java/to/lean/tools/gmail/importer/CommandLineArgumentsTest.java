package to.lean.tools.gmail.importer;

import org.junit.Test;
import static org.junit.Assert.*;

public class CommandLineArgumentsTest {

    @Test
    public void testDefaults() {
        CommandLineArguments args = new CommandLineArguments();
        assertNull(args.mailboxFileName);
        assertEquals("me", args.user);
        assertNull(args.maxMessages);
        assertEquals("/resources/client_secret.json", args.clientSecretResourcePath);
    }

    @Test
    public void testSetArguments() {
        CommandLineArguments args = new CommandLineArguments();
        args.mailboxFileName = "/tmp/mail";
        args.user = "user@example.com";
        args.maxMessages = 10;
        args.clientSecretResourcePath = "/custom/path/secret.json";
        assertEquals("/tmp/mail", args.mailboxFileName);
        assertEquals("user@example.com", args.user);
        assertEquals((Integer)10, args.maxMessages);
        assertEquals("/custom/path/secret.json", args.clientSecretResourcePath);
    }
}