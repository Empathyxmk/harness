package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class ParsingTest {
    private static final Map<String, Object> baseTransaction;
    static {
        baseTransaction = new HashMap<>();
        baseTransaction.put("id", "12c77a49-21c2-427d-8662-beba354e8356");
        baseTransaction.put("__typename", "GenericFeedEvent");
        baseTransaction.put("title", "Transferência enviada");
        baseTransaction.put("detail", "Waldisney da Silva\nR$ 3.668,40");
        baseTransaction.put("postDate", "2021-03-24");
    }

    private Map<String, Object> copyBase() {
        return new HashMap<>(baseTransaction);
    }

    private Map<String, Object> createEdgeTransaction() {
        Map<String, Object> node = new HashMap<>();
        node.put("detail", "");
        node.put("footer", "");
        Map<String, Object> outer = new HashMap<>();
        outer.put("node", node);
        return outer;
    }

    @Test
    void testShouldDoNothingWithTransactionsThatArentPix() {
        Map<String, Object> t = copyBase();
        t.put("__typename", "TransferInEvent");
        t.put("amount", 3429);
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals(t.get("__typename"), parsed.get("__typename"));
        assertEquals(t.get("amount"), parsed.get("amount"));
    }

    @Test
    void testShouldParseInflowPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência recebida");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferInEvent", parsed.get("__typename"));
        assertEquals(3668.40, (Double) parsed.get("amount"), 0.001);
    }

    @Test
    void testShouldParseOutflowPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência enviada");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferOutEvent", parsed.get("__typename"));
        assertEquals(3668.40, (Double) parsed.get("amount"), 0.001);
    }

    @Test
    void testShouldParseReversalPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Reembolso enviado");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferOutReversalEvent", parsed.get("__typename"));
        assertEquals(3668.40, (Double) parsed.get("amount"), 0.001);
    }

    @Test
    void testShouldParseFailedPixTransaction() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência falhou");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("PixTransferFailedEvent", parsed.get("__typename"));
        assertEquals(3668.40, (Double) parsed.get("amount"), 0.001);
    }

    @Test
    void testShouldIgnoreTransactionsWithoutValue() {
        Map<String, Object> t = copyBase();
        t.put("title", "Transferência enviada");
        t.put("detail", "Something without money");
        Map<String, Object> parsed = ParsingUtils.parsePixTransaction(t);
        assertEquals("GenericFeedEvent", parsed.get("__typename"));
        assertNull(parsed.get("amount"));
    }

    @Test
    void testParseGenericTransactionShouldRetrieveAmountFromDetailWhenContainsRs() {
        Map<String, Object> t = createEdgeTransaction();
        ((Map<String, Object>) t.get("node")).put("detail", "R$ 123,56");
        Map<String, Object> parsed = ParsingUtils.parseGenericTransaction(t);
        assertEquals(123.56, (Double) ((Map<String, Object>) parsed.get("node")).get("amount"), 0.001);
    }

    @Test
    void testParseGenericTransactionShouldIgnoreAmountFromDetailWhenDoesntContainRs() {
        Map<String, Object> t = createEdgeTransaction();
        ((Map<String, Object>) t.get("node")).put("detail", "Parabéns !!");
        Map<String, Object> parsed = ParsingUtils.parseGenericTransaction(t);
        assertNull(((Map<String, Object>) parsed.get("node")).get("amount"));
    }

    @Test
    void testParseGenericTransactionShouldRetrieveAmountFromFooterWhenContainsRs() {
        Map<String, Object> t = createEdgeTransaction();
        ((Map<String, Object>) t.get("node")).put("footer", "R$ 1,1");
        Map<String, Object> parsed = ParsingUtils.parseGenericTransaction(t);
        assertEquals(1.1, (Double) ((Map<String, Object>) parsed.get("node")).get("amount"), 0.001);
    }

    @Test
    void testParseGenericTransactionShouldIgnoreAmountFromFooterWhenDoesntContainRs() {
        Map<String, Object> t = createEdgeTransaction();
        ((Map<String, Object>) t.get("node")).put("footer", "Parabéns");
        Map<String, Object> parsed = ParsingUtils.parseGenericTransaction(t);
        assertNull(((Map<String, Object>) parsed.get("node")).get("amount"));
    }

    @Test
    void testParseFloatVariants() {
        assertEquals(1.0, ParsingUtils.parseFloat("R$1,00"), 0.0001);
        assertEquals(0.01, ParsingUtils.parseFloat("R$0,01"), 0.0001);
        assertEquals(0.1, ParsingUtils.parseFloat("R$0,1"), 0.0001);
        assertEquals(1000.20, ParsingUtils.parseFloat("R$1.000,20"), 0.0001);
        assertEquals(83120.11, ParsingUtils.parseFloat("R$83.120,11"), 0.0001);
        assertEquals(9183120.11, ParsingUtils.parseFloat("R$9.183.120,11"), 0.0001);
        assertEquals(0.18, ParsingUtils.parseFloat("Projeção aproximada para 31 de Agosto de 2021, seu dinheiro renderá R$ 0,18"), 0.0001);
    }
}