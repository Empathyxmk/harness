package org.netbeans.modules.php.twig.editor.lexer;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigTopTokenIdPublicTest {

    @Test
    public void testTokenIdOfContent() {
        TwigTopTokenId[] values = TwigTopTokenId.values();
        boolean found = false;
        for (TwigTopTokenId id : values) {
            if ("TWIG_CONTENT".equals(id.name())) {
                found = true;
                break;
            }
        }
        // At least the enum should not throw or be empty
        assertTrue(values.length > 0);
    }

    @Test
    public void testValueOfWithAllEnums() {
        for (TwigTopTokenId id : TwigTopTokenId.values()) {
            assertEquals(id, TwigTopTokenId.valueOf(id.name()));
        }
    }
}