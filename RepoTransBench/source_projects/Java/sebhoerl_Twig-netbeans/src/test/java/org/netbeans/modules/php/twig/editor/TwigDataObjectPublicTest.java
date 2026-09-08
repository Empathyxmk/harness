package org.netbeans.modules.php.twig.editor;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigDataObjectPublicTest {

    @Test
    public void testTwigDataObjectExtensionPublic() {
        TwigDataObject obj = new TwigDataObject("examplePublic.twig");
        assertEquals("twig", obj.getFileExtension());
    }

    @Test
    public void testIsTwigFileReturnsTruePublic() {
        TwigDataObject obj = new TwigDataObject("anotherfilePublic.twig");
        assertTrue(obj.isTwigFile());
    }
}