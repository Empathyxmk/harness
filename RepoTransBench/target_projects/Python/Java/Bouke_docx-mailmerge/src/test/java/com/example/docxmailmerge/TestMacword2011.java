package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestMacword2011 {
    @Test
    public void test_macword2011_merge() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_macword2011.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("User", "MacUser");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}