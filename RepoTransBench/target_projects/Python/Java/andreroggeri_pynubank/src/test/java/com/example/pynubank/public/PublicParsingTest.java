package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class PublicParsingTest {
    private static final Map<String, Object> baseTransaction;
    static {
        baseTransaction = new HashMap<>();
        baseTransaction.put("id", "public-uuid-trans-id");
        baseTransaction.put("__typename", "GenericFeedEvent");
        baseTransaction.put("title", "Transferência enviada");
        baseTransaction.put("detail", "Maria Souza\nR$ 123,00");
        baseTransaction.put("postDate", "2024-06-25");
    }

    private Map<String, Object> copyBase() {
        return new HashMap<>(baseTransaction);
    }

    @Test
    void testShouldParseOutflowPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência enviada");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferOutEvent", parsed.get("__typename"));
        assertEquals(123.0, (Double) parsed.get("amount"), 0.001);
    }

    @Test
    void testShouldParseInflowPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência recebida");
        t.put("detail", "Maria Souza\nR$ 321,50");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferInEvent", parsed.get("__typename"));
        assertEquals(321.5, (Double) parsed.get("amount"), 0.001);
    }
}