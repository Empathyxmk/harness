package org.netbeans.modules.php.twig.editor.parsing;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigParserPublicTest {

    @Test
    public void testParseWhitespacePublic() {
        TwigParser parser = new TwigParser();
        TwigParserResult result = parser.parse("   ");
        assertNotNull(result);
        assertTrue(result.getErrors().isEmpty());
    }

    @Test
    public void testParseOutputTwigPublic() {
        TwigParser parser = new TwigParser();
        String input = "{{ 987 }}";
        TwigParserResult result = parser.parse(input);
        assertNotNull(result);
        assertNotNull(result.getParsedData());
    }
}