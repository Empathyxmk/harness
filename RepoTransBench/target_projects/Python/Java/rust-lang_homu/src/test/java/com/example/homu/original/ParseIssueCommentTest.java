package com.example.homu.original;

import com.example.homu.parse_issue_comment.ParseIssueComment;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ParseIssueCommentTest {

    @Test
    public void testParseCommandCases() {
        ParseIssueComment.Pair<String, String> res1 = ParseIssueComment.parseCommand("@homu: retry");
        assertEquals(new ParseIssueComment.Pair<>("retry", ""), res1);
        ParseIssueComment.Pair<String, String> res2 = ParseIssueComment.parseCommand("@homu: clean foo");
        assertEquals(new ParseIssueComment.Pair<>("clean", "foo"), res2);
    }
}