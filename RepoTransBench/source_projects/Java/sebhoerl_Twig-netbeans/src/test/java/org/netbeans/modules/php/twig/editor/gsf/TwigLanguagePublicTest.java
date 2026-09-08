package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigLanguagePublicTest {

    @Test
    public void testGetMimeTypeIsNotHtml() {
        assertNotEquals("text/html", TwigLanguage.MIME_TYPE);
    }

    @Test
    public void testGetInstanceIsIdentical() {
        TwigLanguage langA = TwigLanguage.getInstance();
        TwigLanguage langB = TwigLanguage.getInstance();
        assertSame(langA, langB);
    }
}