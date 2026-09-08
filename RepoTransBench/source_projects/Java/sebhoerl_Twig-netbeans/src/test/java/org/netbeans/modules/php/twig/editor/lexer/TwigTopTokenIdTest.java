package org.netbeans.modules.php.twig.editor.lexer;

import org.junit.Test;
import static org.junit.Assert.*;
import org.netbeans.api.lexer.Language;

public class TwigTopTokenIdTest {

    @Test
    public void testLanguageNotNull() {
        Language lang = TwigTopTokenId.language();
        assertNotNull(lang);
    }
}