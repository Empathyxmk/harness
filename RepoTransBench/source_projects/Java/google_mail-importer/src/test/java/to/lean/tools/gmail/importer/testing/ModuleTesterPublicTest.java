package to.lean.tools.gmail.importer.testing;

import org.junit.Test;

public class ModuleTesterPublicTest {

    @Test
    public void testDifferentModuleTesterRuns() {
        // Dummy trivial test to ensure ModuleTester is callable
        ModuleTester tester = new ModuleTester();
        tester.test();
    }
}