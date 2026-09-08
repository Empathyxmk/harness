package to.lean.tools.gmail.importer;

import org.junit.Test;
import static org.junit.Assert.*;
import com.google.inject.Guice;
import com.google.inject.Injector;

public class FlagsModulePublicTest {

    @Test
    public void testFlagsModuleProvidesDifferentInstance() {
        CommandLineArguments args = new CommandLineArguments();
        args.mailboxFileName = "/opt/mailbox";
        args.user = "pubuser@domain.com";
        args.maxMessages = 109;
        args.clientSecretResourcePath = "/foo/bar/client_secret_new.json";
        FlagsModule module = new FlagsModule(args);
        Injector injector = Guice.createInjector(module);

        CommandLineArguments injected = injector.getInstance(CommandLineArguments.class);
        assertSame(args, injected);
        assertEquals("/opt/mailbox", injected.mailboxFileName);
        assertEquals("pubuser@domain.com", injected.user);
        assertEquals((Integer)109, injected.maxMessages);
        assertEquals("/foo/bar/client_secret_new.json", injected.clientSecretResourcePath);
    }
}