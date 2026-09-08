package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestIssue8 {
    @Test
    public void test_issue8_mail_merge_page_number() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_issue8.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Address", "123 Main St");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}