package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;
import org.netbeans.modules.csl.api.CodeCompletionHandler;
import org.netbeans.modules.csl.api.Formatter;
import org.netbeans.modules.csl.api.StructureScanner;

public class TwigLanguageTest {

    @Test
    public void testDisplayName() {
        TwigLanguage lang = new TwigLanguage();
        assertEquals("Twig", lang.getDisplayName());
        assertEquals("twig", lang.getPreferredExtension());
    }

    @Test
    public void testIsIdentifierChar() {
        TwigLanguage lang = new TwigLanguage();
        assertTrue(lang.isIdentifierChar('a'));
        assertFalse(lang.isIdentifierChar('1'));
        assertFalse(lang.isIdentifierChar('*'));
    }

    @Test
    public void testGetCompletionHandlerAndFormatter() {
        TwigLanguage lang = new TwigLanguage();
        CodeCompletionHandler cch = lang.getCompletionHandler();
        assertNotNull(cch);
        Formatter formatter = lang.getFormatter();
        assertNotNull(formatter);
    }

    @Test
    public void testHasStructureScannerAndHintsProvider() {
        TwigLanguage lang = new TwigLanguage();
        assertTrue(lang.hasStructureScanner());
        assertFalse(lang.hasHintsProvider());
        StructureScanner ss = lang.getStructureScanner();
        assertNotNull(ss);
    }

    @Test
    public void testIsUsingCustomEditorKitAndHasFormatter() {
        TwigLanguage lang = new TwigLanguage();
        assertTrue(lang.isUsingCustomEditorKit());
        assertTrue(lang.hasFormatter());
    }
}