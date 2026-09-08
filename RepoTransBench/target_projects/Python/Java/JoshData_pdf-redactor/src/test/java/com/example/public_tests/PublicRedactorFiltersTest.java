package com.example.public_tests;

import com.example.pdfredactor.RedactorOptions;
import com.example.pdfredactor.PdfRedactor;
import org.junit.jupiter.api.Test;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.*;
import java.util.function.Function;
import static org.junit.jupiter.api.Assertions.*;

public class PublicRedactorFiltersTest {
    @Test
    public void testFilterCallableReplacement() throws Exception {
        String pdfIn = "%PDF-1.4\nSSN 159-46-2879\n%%EOF";
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(pdfIn.getBytes());
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(new Object[]{
            "\\d{3}-\\d{2}-\\d{4}", (Function<java.util.regex.Matcher, String>)m -> "MASKED"
        });
        PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        assertTrue(options.outputStream.toString().contains("MASKED"));
    }

    @Test
    public void testFilterNonCallableReplacement() throws Exception {
        String pdfIn = "%PDF-1.4\nName: Angela Bailey\n%%EOF";
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(pdfIn.getBytes());
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(new Object[]{
            "Angela Bailey", "AnonName"
        });
        PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        assertTrue(options.outputStream.toString().contains("AnonName"));
    }
}