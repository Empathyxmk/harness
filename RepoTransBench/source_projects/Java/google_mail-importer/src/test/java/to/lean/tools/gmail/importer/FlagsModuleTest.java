package to.lean.tools.gmail.importer;

import com.google.inject.Guice;
import com.google.inject.Injector;
import org.junit.Test;
import static org.junit.Assert.*;

public class FlagsModuleTest {
    @Test
    public void testFlagsModuleBindsArguments() {
        CommandLineArguments args = new CommandLineArguments();
        args.mailboxFileName = "foo";
        Injector injector = Guice.createInjector(new FlagsModule(args));
        CommandLineArguments injected = injector.getInstance(CommandLineArguments.class);
        assertEquals("foo", injected.mailboxFileName);
        // They should be the same instance
        assertSame(args, injected);
    }
}