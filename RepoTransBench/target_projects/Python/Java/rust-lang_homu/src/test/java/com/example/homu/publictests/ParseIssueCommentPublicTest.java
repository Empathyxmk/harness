package com.example.homu.publictests;

import com.example.homu.parse_issue_comment.ParseIssueComment;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ParseIssueCommentPublicTest {

    @Test
    public void testParseCommandCustomCase() {
        ParseIssueComment.Pair<String, String> pair = ParseIssueComment.parseCommand("@homu: test-queue");
        assertEquals(new ParseIssueComment.Pair<>("test-queue", ""), pair);
    }

    @Test
    public void testParseCommandArgumented() {
        ParseIssueComment.Pair<String, String> pair = ParseIssueComment.parseCommand("@homu: clean bar");
        assertEquals(new ParseIssueComment.Pair<>("clean", "bar"), pair);
    }
}