package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestMultipleElements {
    @Test
    public void test_multiple_elements_docx() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_multiple_elements.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Elem1", "One");
            put("Elem2", "Two");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}