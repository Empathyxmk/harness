package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestMergePages {
    @Test
    public void test_merge_pages_multiple() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_merge_pages.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Recipient", "RecipientName");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}