package com.example.public_tests;

import com.example.pdfredactor.RedactorOptions;
import com.example.pdfredactor.PdfRedactor;
import org.junit.jupiter.api.Test;
import java.util.*;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.function.Function;

import static org.junit.jupiter.api.Assertions.*;

public class PublicRedactorTest {

    @Test
    public void testBasicRedaction() throws Exception {
        String pdfText = "%PDF-1.4\n% Public test: secret12345 replaced\nxyz 654-32-1987 zyx\n%%EOF";
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(pdfText.getBytes());
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(new Object[]{
                "\\b654-32-1987\\b",
                (Function<java.util.regex.Matcher, String>)(m -> "[REDACTED-ID]")
        });
        PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        byte[] result = ((ByteArrayOutputStream)options.outputStream).toByteArray();
        assertTrue(new String(result).contains("[REDACTED-ID]"));
    }

    @Test
    public void testUnicodeFilter() throws Exception {
        String pdfText = "%PDF-1.4\nUnusual symbol: §\nID 88-99-7766\n%%EOF";
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(pdfText.getBytes());
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(new Object[]{
            "\\b88-99-7766\\b",
            (Function<java.util.regex.Matcher, String>)m -> "<REMOVED>"
        });
        PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        byte[] result = ((ByteArrayOutputStream)options.outputStream).toByteArray();
        assertTrue(new String(result).contains("<REMOVED>"));
    }

    @Test
    public void testMultilineFilter() throws Exception {
        String pdfText = "%PDF-1.4\nFirstLine\nID: 222-33-4444\nSecondLine\n%%EOF";
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(pdfText.getBytes());
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(new Object[]{
            "222-33-4444",
            (Function<java.util.regex.Matcher, String>)m -> "*****"
        });
        PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        byte[] result = ((ByteArrayOutputStream)options.outputStream).toByteArray();
        assertTrue(new String(result).contains("*****"));
    }
}