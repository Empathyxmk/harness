package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;

public class TwigStructureScannerPublicTest {

    @Test
    public void testScanEmptyReturnsListPublic() {
        TwigStructureScanner scanner = new TwigStructureScanner();
        assertTrue(scanner.scan("", null).isEmpty());
    }

    @Test
    public void testGetHeaderReturnsNullPublic() {
        TwigStructureScanner scanner = new TwigStructureScanner();
        assertNull(scanner.getHeader(""));
    }
}