package org.netbeans.modules.php.twig.editor.parsing;

import org.junit.Test;
import static org.junit.Assert.*;
import org.netbeans.modules.parsing.api.Snapshot;
import org.netbeans.modules.parsing.spi.ParseException;
import org.netbeans.modules.parsing.spi.Parser;
import org.netbeans.modules.php.twig.editor.parsing.TwigParser;
import org.netbeans.modules.php.twig.editor.parsing.TwigParserResult;

public class TwigParserTest {

    @Test
    public void testParseGetResult() throws ParseException {
        Parser parser = new TwigParser();
        Snapshot snapshot = null;
        Parser.Result result = parser.parse(snapshot, null, null);
        assertNotNull(result);
        assertTrue(result instanceof TwigParserResult);

        Parser.Result r1 = parser.getResult(null);
        assertNotNull(r1);
        assertTrue(r1 instanceof TwigParserResult);
    }
}