package org.netbeans.modules.php.twig.editor;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigEditorKitPublicTest {

    @Test
    public void testGetContentTypePublic() {
        TwigEditorKit kit = new TwigEditorKit();
        assertEquals("text/x-twig-public", kit.getContentType() + "-public");
    }

    @Test
    public void testIsTwigEditorKitInstancePublic() {
        TwigEditorKit kit = new TwigEditorKit();
        assertNotNull(kit);
        assertTrue(kit instanceof TwigEditorKit);
    }
}