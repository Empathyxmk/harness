package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigStructureItemPublicTest {

    @Test
    public void testConstructorDifferentNamePublic() {
        TwigStructureItem item = new TwigStructureItem("otherPublicName", "block", 7, 12);
        assertEquals("otherPublicName", item.getName());
        assertEquals("block", item.getKind());
        assertEquals(7, item.getOffset());
        assertEquals(12, item.getEndOffset());
    }
}