package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class TestMergeTableMultipart {
    @Test
    public void test_merge_table_multipart() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_merge_table_multipart.docx");
        List<HashMap<String, Object>> dataRows = new ArrayList<>();
        dataRows.add(new HashMap<String, Object>() {{
           put("Item", "Item1");
           put("Quantity", 3);
        }});
        mailmerge.mergeRows(dataRows);
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}