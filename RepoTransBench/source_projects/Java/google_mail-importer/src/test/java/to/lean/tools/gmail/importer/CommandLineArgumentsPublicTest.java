package to.lean.tools.gmail.importer;

import org.junit.Test;
import static org.junit.Assert.*;

public class CommandLineArgumentsPublicTest {

    @Test
    public void testDefaultsPublic() {
        CommandLineArguments args = new CommandLineArguments();
        assertNull(args.mailboxFileName);
        assertEquals("me", args.user);
        assertNull(args.maxMessages);
        assertEquals("/resources/client_secret.json", args.clientSecretResourcePath);
    }

    @Test
    public void testSetArgumentsPublic() {
        CommandLineArguments args = new CommandLineArguments();
        args.mailboxFileName = "/var/mail";
        args.user = "anotheruser@domain.com";
        args.maxMessages = 42;
        args.clientSecretResourcePath = "/different/path/secret_v2.json";
        assertEquals("/var/mail", args.mailboxFileName);
        assertEquals("anotheruser@domain.com", args.user);
        assertEquals((Integer)42, args.maxMessages);
        assertEquals("/different/path/secret_v2.json", args.clientSecretResourcePath);
    }
}