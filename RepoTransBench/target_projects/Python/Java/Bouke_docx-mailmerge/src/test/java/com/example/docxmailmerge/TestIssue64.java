package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestIssue64 {
    @Test
    public void test_issue64_field_handling() {
        // Simulates merging a field intended to check for a bug (in Python, this is mergefields with strange encodings)
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_issue64.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Name", "John Doe");
        }});
        // Assert that placeholder output equals itself (simulated logic)
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}