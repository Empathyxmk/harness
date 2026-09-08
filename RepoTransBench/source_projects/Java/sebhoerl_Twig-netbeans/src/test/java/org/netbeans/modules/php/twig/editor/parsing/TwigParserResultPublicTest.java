package org.netbeans.modules.php.twig.editor.parsing;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigParserResultPublicTest {

    @Test
    public void testBlankInputPublic() {
        TwigParserResult result = new TwigParserResult("   ");
        assertTrue(result.getErrors().isEmpty());
        assertNotNull(result.getParsedData());
    }

    @Test
    public void testSimpleTwigInputPublic() {
        TwigParserResult result = new TwigParserResult("{% include 'header.twig' %}");
        assertNotNull(result.getParsedData());
        assertNotNull(result.getErrors());
    }
}