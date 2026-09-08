package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.HashMap;

public class TestWinword2010 {
    @Test
    public void test_winword2010_integration() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_winword2010.docx");
        mailmerge.mergeFields(new HashMap<String, Object>() {{
            put("Special", "Winword");
        }});
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}