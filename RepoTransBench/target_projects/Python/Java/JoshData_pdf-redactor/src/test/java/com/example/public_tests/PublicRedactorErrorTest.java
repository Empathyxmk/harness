package com.example.public_tests;

import com.example.pdfredactor.RedactorOptions;
import com.example.pdfredactor.PdfRedactor;
import org.junit.jupiter.api.Test;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicRedactorErrorTest {

    @Test
    public void testInvalidFilterTypeError() {
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream(new byte[0]);
        options.outputStream = new ByteArrayOutputStream();
        options.contentFilters = Arrays.asList(
            new Object[]{12345, "foo"} // invalid pattern type
        );
        assertThrows(Exception.class, () -> {
            PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        });
    }

    @Test
    public void testInvalidOutputStream() {
        RedactorOptions options = new RedactorOptions();
        options.inputStream = new ByteArrayInputStream("%PDF-1.3".getBytes());
        options.outputStream = null; // Pass null to cause error
        options.contentFilters = new ArrayList<>();
        assertThrows(Exception.class, () -> {
            PdfRedactor.redactor(options, options.inputStream, options.outputStream);
        });
    }
}