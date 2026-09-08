package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import com.example.docxmailmerge.util.FakeMailmerge;
import com.example.docxmailmerge.util.DocxAssert;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class TestMergeTableRows {
    @Test
    public void test_merge_table_rows() {
        FakeMailmerge mailmerge = new FakeMailmerge("tests/test_merge_table_rows.docx");
        List<HashMap<String, Object>> dataRows = new ArrayList<>();
        dataRows.add(new HashMap<String, Object>() {{
           put("Name", "Anna");
           put("Score", 95);
        }});
        mailmerge.mergeRows(dataRows);
        DocxAssert.assertEqualDocx(mailmerge.getMergedDocument(), mailmerge.getMergedDocument());
    }
}