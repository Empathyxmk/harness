package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestMergeTemplates {
    @Test
    public void test_merge_templates() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_merge_templates_simple.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Title", "Report");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}