package org.netbeans.modules.php.twig.editor;

import org.junit.Test;
import static org.junit.Assert.*;
import javax.swing.text.Document;

public class TwigEditorKitTest {

    @Test
    public void testContentType() {
        TwigEditorKit kit = new TwigEditorKit();
        assertEquals("text/twig", kit.getContentType());
    }

    @Test
    public void testCreateDefaultDocument() {
        TwigEditorKit kit = new TwigEditorKit();
        Document doc = kit.createDefaultDocument();
        assertNotNull(doc);
    }
}