package org.netbeans.modules.php.twig.editor.format;

import org.junit.Test;
import static org.junit.Assert.*;
import org.netbeans.modules.csl.api.CodeCompletionHandler;
import org.netbeans.modules.csl.api.Formatter;

public class TwigFormatterTest {

    @Test
    public void testFormatterExists() {
        TwigFormatter formatter = new TwigFormatter();
        assertNotNull(formatter);
    }
}