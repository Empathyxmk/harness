package com.example.public_tests;

import com.example.rdflibjsonld.RdflibJsonld;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.*;
import java.util.Locale;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_version_and_metadata.py
 */
public class PublicVersionAndMetadataTest {

    @Test
    public void testModuleHasVersion() {
        assertNotNull(RdflibJsonld.__version__);
        String ver = RdflibJsonld.__version__;
        assertTrue(ver instanceof String);
        long dotCount = ver.chars().filter(c -> c == '.').count();
        assertTrue(dotCount >= 1, "Version must contain at least one dot");
    }

    @Test
    public void testModuleAuthorAndContact() {
        assertNotNull(RdflibJsonld.__author__);
        String author = RdflibJsonld.__author__;
        assertNotNull(author);
        assertTrue(author instanceof String);

        assertNotNull(RdflibJsonld.__contact__);
        String contact = RdflibJsonld.__contact__;
        assertTrue(contact.contains("@") && contact.contains("."),
            "Contact should look like an email");
    }

    @Test
    public void testSetupPyHasImportOrClass() throws IOException {
        Path setupPy = Paths.get("setup.py").toAbsolutePath();
        assertTrue(Files.exists(setupPy), "setup.py not found");
        String contents = new String(Files.readAllBytes(setupPy));
        String lowered = contents.toLowerCase(Locale.ROOT);
        assertTrue(lowered.contains("import") || lowered.contains("class"),
            "setup.py should contain either 'import' or 'class'");
    }

    @Test
    public void testModuleDocstringMentionsJsonld() {
        String doc = RdflibJsonld.__doc__;
        assertNotNull(doc);
        String docLower = doc.toLowerCase(Locale.ROOT);
        assertTrue(
                docLower.contains("jsonld") || docLower.contains("json-ld"),
                "Docstring should mention jsonld or json-ld"
        );
    }
}