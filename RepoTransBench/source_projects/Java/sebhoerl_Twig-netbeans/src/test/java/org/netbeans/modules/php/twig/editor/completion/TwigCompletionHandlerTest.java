package org.netbeans.modules.php.twig.editor.completion;

import org.junit.Test;
import javax.swing.text.Document;
import javax.swing.text.JTextComponent;
import org.netbeans.modules.csl.api.CodeCompletionContext;
import org.netbeans.modules.csl.api.CodeCompletionResult;
import org.netbeans.modules.csl.api.CompletionProposal;
import org.netbeans.modules.csl.api.ElementHandle;
import org.netbeans.modules.csl.api.ParameterInfo;
import org.netbeans.modules.csl.api.CodeCompletionHandler.QueryType;
import org.netbeans.modules.csl.spi.ParserResult;

import static org.junit.Assert.*;
import java.util.*;

public class TwigCompletionHandlerTest {

    TwigCompletionHandler handler = new TwigCompletionHandler();

    @Test
    public void testCompleteReturnsNONE() {
        CodeCompletionContext ccc = null;
        CodeCompletionResult result = handler.complete(ccc);
        assertEquals(CodeCompletionResult.NONE, result);
    }

    @Test
    public void testDocumentIsEmpty() {
        assertEquals("", handler.document(null, null));
    }

    @Test
    public void testResolveLinkIsNull() {
        assertNull(handler.resolveLink("foo", null));
    }

    @Test
    public void testGetPrefixIsEmpty() {
        assertEquals("", handler.getPrefix(null, 0, true));
    }

    @Test
    public void testAutoQuery() {
        JTextComponent jtc = null;
        assertEquals(QueryType.ALL_COMPLETION, handler.getAutoQuery(jtc, "foo"));
    }

    @Test
    public void testResolveTemplateVariable() {
        assertNull(handler.resolveTemplateVariable("foo", null, 1, "bar", Collections.emptyMap()));
    }

    @Test
    public void testGetApplicableTemplates() {
        Set<String> result = handler.getApplicableTemplates(null, 1, 2);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testParameters() {
        ParameterInfo pi = handler.parameters(null, 1, null);
        assertNotNull(pi);
        assertEquals(0, pi.getInsertIndex());
        assertEquals(0, pi.getOffset());
        assertTrue(pi.getParameters().isEmpty());
    }
}